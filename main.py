import argparse
import configparser
from pathlib import Path

import joblib

from src.function_loader import FunctionLoader
from src.transpiler import Transpiler
from src.utils import load_torch_state_dict


def _load_model(path: Path):
    if str(path).endswith(".joblib"):
        return joblib.load(path)
    elif str(path).endswith(".pt"):
        return load_torch_state_dict(path)
    else:
        raise ValueError("Unsupported model file format.")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transpile a model to C and/or Verilog"
    )
    parser.add_argument(
        "--path",
        required=True,
        type=Path,
        help="Path to the model file (.joblib or .pt)",
    )
    parser.add_argument("--c", action="store_true", dest="to_c", help="Transpile to C")
    parser.add_argument(
        "--v", action="store_true", dest="to_v", help="Transpile to Verilog"
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    if not args.path.exists():
        raise FileNotFoundError(f"Model path not found: {args.path}")

    targets = []
    if args.to_c:
        targets.append("c")
    if args.to_v:
        targets.append("verilog")
    if not targets:
        # Default to both if no explicit language flags provided
        targets = ["c", "verilog"]

    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])

    model = _load_model(args.path)
    for language in targets:
        output_ext = "c" if language == "c" else "v"
        output_file = Path(f"outputs/{args.path.stem}.{output_ext}")
        transpiler = Transpiler(model=model, language=language, output_file=output_file)
        transpiler.transpile(function_loader=function_loader)


if __name__ == "__main__":
    main()
