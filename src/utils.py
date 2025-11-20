from pathlib import Path

import joblib
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from src.metadata_retriever.metadata_retriever import (
    DecisionTreeClassifierMetadataRetriever,
    LinearRegressionMetadataRetriever,
    LogisticRegressionMetadataRetriever,
    MetadataRetriever,
)


def load_models(paths) -> list:
    models = []
    for path in paths:
        model = joblib.load(path)
        models.append(model)
    return models


def write_to_file(path: Path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w+") as f:
        f.write(content)
    return path


def get_metadata_retriever_class(model) -> type:
    util = MetadataRetriever(model=model, language=None)
    util_model = util._get_model()
    if isinstance(util_model, LinearRegression):
        return LinearRegressionMetadataRetriever
    elif isinstance(util_model, LogisticRegression):
        return LogisticRegressionMetadataRetriever
    elif isinstance(util_model, DecisionTreeClassifier):
        return DecisionTreeClassifierMetadataRetriever
    else:
        raise ValueError(f"Unsupported model type: {type(util_model)}")
