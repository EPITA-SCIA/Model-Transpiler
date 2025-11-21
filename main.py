import configparser
from pathlib import Path

import joblib
import torch

from src.function_loader import FunctionLoader
from src.transpiler import Transpiler


def _load_model(path: Path):
    if str(path).endswith(".joblib"):
        return joblib.load(path)
    elif str(path).endswith(".pth"):
        return torch.load(path)
    else:
        raise ValueError("Unsupported model file format.")


def main():
    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])

    model = _load_model(Path("models/logistic_multi.joblib"))
    transpiler = Transpiler(
        model=model,
        language="verilog",
        output_file=Path("output.v"),
    )
    transpiler.transpile(function_loader=function_loader)


if __name__ == "__main__":
    main()
