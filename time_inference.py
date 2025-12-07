import argparse
from pathlib import Path

import joblib
import torch

from src.utils import load_torch_state_dict


def _load_model(path: Path):
    if str(path).endswith(".joblib"):
        return joblib.load(path)
    elif str(path).endswith(".pt"):
        return load_torch_state_dict(path)
    else:
        raise ValueError("Unsupported model file format.")


def _infer_inputs(model, explicit_inputs):
    if explicit_inputs:
        return explicit_inputs

    if hasattr(model, "n_features_in_"):
        n_features = int(getattr(model, "n_features_in_", 1))
    elif isinstance(model, torch.nn.Sequential) and len(model) > 0:
        first = model[0]
        n_features = int(getattr(first, "in_features", 1))
    else:
        n_features = 3

    return [float(i + 1) for i in range(n_features)]


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Run a single Python inference for a model"
    )
    parser.add_argument(
        "--path",
        required=True,
        type=Path,
        help="Path to the model file (.joblib or .pt)",
    )
    parser.add_argument(
        "--inputs",
        nargs="*",
        type=float,
        default=None,
        help="Optional input values; defaults to 1..n_features",
    )
    return parser.parse_args()


def main():
    args = _parse_args()
    if not args.path.exists():
        raise FileNotFoundError(f"Model path not found: {args.path}")
    model = _load_model(args.path)
    inputs = _infer_inputs(model, args.inputs)

    try:
        tensor_inputs = torch.tensor(inputs, dtype=torch.float32)
        with torch.no_grad():
            output = model(tensor_inputs)
    except Exception:
        output = model.predict([inputs])

    print(f"Model: {args.path.name}")
    print(f"Inputs: {inputs}")
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
