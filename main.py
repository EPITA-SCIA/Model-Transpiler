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
    print(function_loader["c"]["regular"]["includes"])
    print("\n".join(metadata))
    dependencies = get_dependencies("decision_tree")
    for dep in dependencies:
        print(function_loader["c"]["regular"][dep])
    print(function_loader["c"]["regular"]["decision_tree"])
    print(function_loader["c"]["main"]["decision_tree"])


if __name__ == "__main__":
    main()
