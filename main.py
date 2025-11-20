import configparser
from pathlib import Path

import joblib

from src.function_loader import FunctionLoader
from src.transpiler import Transpiler


def main():
    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])

    model = joblib.load("tests/tree.joblib")
    transpiler = Transpiler(
        model=model,
        language="verilog",
        output_file=Path("output.v"),
    )
    transpiler.transpile(function_loader=function_loader)


if __name__ == "__main__":
    main()
