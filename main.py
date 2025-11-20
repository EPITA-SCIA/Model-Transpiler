import configparser
from src.function_loader import FunctionLoader
import joblib
from pathlib import Path

from src.transpiler import Transpiler

def main():
    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])

    model = joblib.load("tests/tree.joblib")
    transpiler = Transpiler(
        model=model,
        language="c",
        output_file=Path("output.c"),
    )
    transpiler.transpile(function_loader=function_loader)

if __name__ == "__main__":
    main()
