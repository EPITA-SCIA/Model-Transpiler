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


def main():
    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])

    model = _load_model(Path("models/mlp_model.pt"))
    transpiler = Transpiler(
        model=model,
        language="c",
        output_file=Path("output.c"),
    )
    transpiler.transpile(function_loader=function_loader)


if __name__ == "__main__":
    main()
