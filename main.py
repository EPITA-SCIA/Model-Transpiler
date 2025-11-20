import configparser
from src.function_loader import FunctionLoader
from src.dependencies import get_dependencies
from src.metadata_retriever.metadata_retriever import MetadataRetriever
import joblib

def main():
    conf = configparser.ConfigParser()
    conf.read(".config")

    function_loader = FunctionLoader(conf["FunctionLoader"])

    model = joblib.load("tests/tree.joblib")
    metadata_retriever = MetadataRetriever(model=model, language="c")
    metadata = metadata_retriever.retrieve_metadata()
    print(metadata)
    # dependencies = get_dependencies("logistic_regression")
    # print(dependencies)
    # hardcode values
    # for dep in dependencies:
    #     # Here you would do something with the loaded dependency
    #     # For demonstration, we just print its content
    #     print(function_loader["c"]["regular"][dep])
    # print(function_loader["c"]["regular"]["logistic_regression"])
    # print(function_loader["c"]["main"]["logistic_regression"])


if __name__ == "__main__":
    main()
