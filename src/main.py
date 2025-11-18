import configparser
from function_loader import FunctionLoader


def main():
    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])
    print(function_loader["c"]["linear_regression"])


if __name__ == "__main__":
    main()
