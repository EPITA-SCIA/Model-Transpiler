import configparser
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import joblib
import numpy as np
import pytest
import torch

# Ensure repository root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.function_loader import FunctionLoader  # noqa: E402
from src.transpiler import Transpiler  # noqa: E402

CONFIG_PATH = ROOT / ".config"
MODELS_DIR = ROOT / "models"


def _load_function_loader() -> FunctionLoader:
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)
    return FunctionLoader(config["FunctionLoader"])


def _transpile_model(
    model_path: Path, language: str, output_path: Path, fl: FunctionLoader
):
    if model_path.suffix in {".pt", ".pth"}:
        from src.utils import load_torch_state_dict

        model = load_torch_state_dict(model_path)
    else:
        model = joblib.load(model_path)
    transpiler = Transpiler(model=model, language=language, output_file=output_path)
    transpiler.transpile(function_loader=fl)


def _require_tool(tool: str):
    if shutil.which(tool) is None:
        pytest.skip(f"'{tool}' not available in PATH")


def _compile_c(source: Path, binary: Path):
    _require_tool("gcc")
    subprocess.run(
        ["gcc", "-std=c99", str(source), "-lm", "-o", str(binary)],
        check=True,
        capture_output=True,
        text=True,
    )


def _compile_verilog(source: Path, binary: Path):
    _require_tool("iverilog")
    subprocess.run(
        ["iverilog", "-o", str(binary), str(source)],
        check=True,
        capture_output=True,
        text=True,
    )


def _make_inputs(model) -> list[float]:
    """Generate deterministic non-zero inputs based on the model feature count."""
    n_features = int(getattr(model, "n_features_in_", 1))
    return [float(i + 1) for i in range(n_features)]


def _run_and_parse_prediction(cmd: list[str]) -> float:
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    match = re.search(r"Prediction:\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)", proc.stdout)
    if not match:
        raise AssertionError(
            f"Could not parse prediction from output:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )
    return float(match.group(1))


def _run_and_parse_prediction_and_class(cmd: list[str]):
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    pred_match = re.search(
        r"Prediction:\s*([+-]?\d*\.?\d+(?:[eE][+-]?\d+)?)", proc.stdout
    )
    class_match = re.search(r"Predicted class:\s*(.+)", proc.stdout)
    pred_val = float(pred_match.group(1)) if pred_match else None
    class_val = class_match.group(1).strip() if class_match else None
    return pred_val, class_val


def test_transpiler_runs_all_models():
    fl = _load_function_loader()
    for model_path in MODELS_DIR.glob("*.joblib"):
        for language in ("c", "verilog"):
            with tempfile.TemporaryDirectory() as tmpdir:
                output_ext = "c" if language == "c" else "v"
                output_path = Path(tmpdir) / f"{model_path.stem}.{output_ext}"
                _transpile_model(model_path, language, output_path, fl)
                assert output_path.exists(), (
                    f"{language} output not generated for {model_path.name}"
                )


def test_generated_sources_compile():
    fl = _load_function_loader()
    for model_path in MODELS_DIR.glob("*.joblib"):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            c_source = tmpdir_path / f"{model_path.stem}.c"
            v_source = tmpdir_path / f"{model_path.stem}.v"
            _transpile_model(model_path, "c", c_source, fl)
            _transpile_model(model_path, "verilog", v_source, fl)

            _compile_c(c_source, tmpdir_path / f"{model_path.stem}_c.out")
            _compile_verilog(v_source, tmpdir_path / f"{model_path.stem}_v.out")


def test_linear_outputs_match_python_c_verilog():
    # Use the linear regression model as the default cross-check target
    fl = _load_function_loader()
    linear_model_path = MODELS_DIR / "linear.joblib"
    model = joblib.load(linear_model_path)
    inputs = _make_inputs(model)  # simple deterministic inputs

    python_pred = float(model.predict([inputs])[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "linear.c"
        v_source = tmpdir_path / "linear.v"
        c_bin = tmpdir_path / "linear_c.out"
        v_bin = tmpdir_path / "linear_v.out"

        _transpile_model(linear_model_path, "c", c_source, fl)
        _transpile_model(linear_model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        arg_list = [str(val) for val in inputs]
        c_pred = _run_and_parse_prediction([str(c_bin), *arg_list])
        v_pred = _run_and_parse_prediction([str(v_bin), *arg_list])

    tolerance = 1e-5
    assert abs(c_pred - python_pred) < tolerance, "C prediction diverges from Python"
    assert abs(v_pred - python_pred) < tolerance, (
        "Verilog prediction diverges from Python"
    )


def test_logistic_binary_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "logistic_binary.joblib"
    model = joblib.load(model_path)
    inputs = _make_inputs(model)

    python_prob = float(model.predict_proba([inputs])[0][1])
    python_class = str(model.predict([inputs])[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "logistic_bin.c"
        v_source = tmpdir_path / "logistic_bin.v"
        c_bin = tmpdir_path / "logistic_bin_c.out"
        v_bin = tmpdir_path / "logistic_bin_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args = [str(val) for val in inputs]
        c_pred, c_class = _run_and_parse_prediction_and_class([str(c_bin), *args])
        v_pred, v_class = _run_and_parse_prediction_and_class([str(v_bin), *args])

    tol = 1e-3
    assert abs(c_pred - python_prob) < tol
    assert abs(v_pred - python_prob) < tol
    assert c_class == python_class
    assert v_class == python_class


def test_logistic_multi_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "logistic_multi.joblib"
    model = joblib.load(model_path)
    inputs = _make_inputs(model)

    python_class = str(model.predict([inputs])[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "logistic_multi.c"
        v_source = tmpdir_path / "logistic_multi.v"
        c_bin = tmpdir_path / "logistic_multi_c.out"
        v_bin = tmpdir_path / "logistic_multi_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args = [str(val) for val in inputs]
        _, c_class = _run_and_parse_prediction_and_class([str(c_bin), *args])
        _, v_class = _run_and_parse_prediction_and_class([str(v_bin), *args])

    assert c_class == python_class
    assert v_class == python_class


def test_tree_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "tree.joblib"
    model = joblib.load(model_path)
    inputs = np.array(_make_inputs(model)).reshape(1, -1)

    python_class = str(model.predict(inputs)[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "tree.c"
        v_source = tmpdir_path / "tree.v"
        c_bin = tmpdir_path / "tree_c.out"
        v_bin = tmpdir_path / "tree_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args = [str(val) for val in inputs.flatten()]
        _, c_class = _run_and_parse_prediction_and_class([str(c_bin), *args])
        _, v_class = _run_and_parse_prediction_and_class([str(v_bin), *args])

    assert c_class == python_class
    assert v_class == python_class


def test_linear_minmax_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "linear_minmax.joblib"
    model = joblib.load(model_path)
    base_inputs = _make_inputs(model)
    out_inputs = [x + 10.0 for x in base_inputs]
    python_pred = float(model.predict([base_inputs])[0])
    python_pred_out = float(model.predict([out_inputs])[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "linear_mm.c"
        v_source = tmpdir_path / "linear_mm.v"
        c_bin = tmpdir_path / "linear_mm_c.out"
        v_bin = tmpdir_path / "linear_mm_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args_base = [str(val) for val in base_inputs]
        args_out = [str(val) for val in out_inputs]
        c_pred = _run_and_parse_prediction([str(c_bin), *args_base])
        v_pred = _run_and_parse_prediction([str(v_bin), *args_base])
        c_pred_out = _run_and_parse_prediction([str(c_bin), *args_out])
        v_pred_out = _run_and_parse_prediction([str(v_bin), *args_out])

    tol = 1e-5
    assert abs(c_pred - python_pred) < tol
    assert abs(v_pred - python_pred) < tol
    assert abs(c_pred_out - python_pred_out) < tol
    assert abs(v_pred_out - python_pred_out) < tol


def test_logistic_binary_minmax_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "logistic_binary_minmax.joblib"
    model = joblib.load(model_path)
    base_inputs = _make_inputs(model)
    out_inputs = [x + 10.0 for x in base_inputs]

    python_prob = float(model.predict_proba([base_inputs])[0][1])
    python_class = str(model.predict([base_inputs])[0])
    python_prob_out = float(model.predict_proba([out_inputs])[0][1])
    python_class_out = str(model.predict([out_inputs])[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "logistic_bin_mm.c"
        v_source = tmpdir_path / "logistic_bin_mm.v"
        c_bin = tmpdir_path / "logistic_bin_mm_c.out"
        v_bin = tmpdir_path / "logistic_bin_mm_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args_base = [str(val) for val in base_inputs]
        args_out = [str(val) for val in out_inputs]
        c_pred, c_class = _run_and_parse_prediction_and_class([str(c_bin), *args_base])
        v_pred, v_class = _run_and_parse_prediction_and_class([str(v_bin), *args_base])
        c_pred_out, c_class_out = _run_and_parse_prediction_and_class([str(c_bin), *args_out])
        v_pred_out, v_class_out = _run_and_parse_prediction_and_class([str(v_bin), *args_out])

    tol = 1e-3
    assert abs(c_pred - python_prob) < tol
    assert abs(v_pred - python_prob) < tol
    assert c_class == python_class
    assert v_class == python_class
    assert abs(c_pred_out - python_prob_out) < tol
    assert abs(v_pred_out - python_prob_out) < tol
    assert c_class_out == python_class_out
    assert v_class_out == python_class_out


def test_logistic_multi_minmax_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "logistic_multi_minmax.joblib"
    model = joblib.load(model_path)
    base_inputs = _make_inputs(model)
    out_inputs = [x + 10.0 for x in base_inputs]
    python_class = str(model.predict([base_inputs])[0])
    python_class_out = str(model.predict([out_inputs])[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "logistic_multi_mm.c"
        v_source = tmpdir_path / "logistic_multi_mm.v"
        c_bin = tmpdir_path / "logistic_multi_mm_c.out"
        v_bin = tmpdir_path / "logistic_multi_mm_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args_base = [str(val) for val in base_inputs]
        args_out = [str(val) for val in out_inputs]
        _, c_class = _run_and_parse_prediction_and_class([str(c_bin), *args_base])
        _, v_class = _run_and_parse_prediction_and_class([str(v_bin), *args_base])
        _, c_class_out = _run_and_parse_prediction_and_class([str(c_bin), *args_out])
        _, v_class_out = _run_and_parse_prediction_and_class([str(v_bin), *args_out])

    assert c_class == python_class
    assert v_class == python_class
    assert c_class_out == python_class_out
    assert v_class_out == python_class_out


def test_tree_minmax_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "tree_minmax.joblib"
    model = joblib.load(model_path)
    base_inputs = np.array(_make_inputs(model)).reshape(1, -1)
    out_inputs = np.array([x + 10.0 for x in _make_inputs(model)]).reshape(1, -1)
    python_class = str(model.predict(base_inputs)[0])
    python_class_out = str(model.predict(out_inputs)[0])

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "tree_mm.c"
        v_source = tmpdir_path / "tree_mm.v"
        c_bin = tmpdir_path / "tree_mm_c.out"
        v_bin = tmpdir_path / "tree_mm_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args_base = [str(val) for val in base_inputs.flatten()]
        args_out = [str(val) for val in out_inputs.flatten()]
        _, c_class = _run_and_parse_prediction_and_class([str(c_bin), *args_base])
        _, v_class = _run_and_parse_prediction_and_class([str(v_bin), *args_base])
        _, c_class_out = _run_and_parse_prediction_and_class([str(c_bin), *args_out])
        _, v_class_out = _run_and_parse_prediction_and_class([str(v_bin), *args_out])

    assert c_class == python_class
    assert v_class == python_class
    assert c_class_out == python_class_out
    assert v_class_out == python_class_out


def test_mlp_state_dict_outputs_match_python_c_verilog():
    fl = _load_function_loader()
    model_path = MODELS_DIR / "mlp_model.pt"
    # Load via our state-dict loader to mirror transpiler behavior
    from src.utils import load_torch_state_dict

    model = load_torch_state_dict(model_path)
    # Simple deterministic inputs sized from first layer
    n_features = model[0].in_features
    base_inputs = [float(i + 1) for i in range(n_features)]
    out_inputs = [x + 5.0 for x in base_inputs]

    python_out = model(torch.tensor([base_inputs], dtype=torch.float32)).detach().numpy()[0]
    python_out_out = model(torch.tensor([out_inputs], dtype=torch.float32)).detach().numpy()[0]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        c_source = tmpdir_path / "mlp.c"
        v_source = tmpdir_path / "mlp.v"
        c_bin = tmpdir_path / "mlp_c.out"
        v_bin = tmpdir_path / "mlp_v.out"

        _transpile_model(model_path, "c", c_source, fl)
        _transpile_model(model_path, "verilog", v_source, fl)
        _compile_c(c_source, c_bin)
        _compile_verilog(v_source, v_bin)

        args_base = [str(val) for val in base_inputs]
        args_out = [str(val) for val in out_inputs]
        c_pred_base = _run_and_parse_prediction([str(c_bin), *args_base])
        v_pred_base = _run_and_parse_prediction([str(v_bin), *args_base])
        c_pred_out = _run_and_parse_prediction([str(c_bin), *args_out])
        v_pred_out = _run_and_parse_prediction([str(v_bin), *args_out])

    # Compare only the first output (network is likely single-output), but apply to all if multi-output
    tol = 1e-4
    assert abs(c_pred_base - float(python_out[0])) < tol
    assert abs(v_pred_base - float(python_out[0])) < tol
    assert abs(c_pred_out - float(python_out_out[0])) < tol
    assert abs(v_pred_out - float(python_out_out[0])) < tol
