from collections import OrderedDict
from pathlib import Path

import joblib
import torch
import torch.nn as nn
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from src.metadata_retriever.metadata_retriever import (
    DecisionTreeClassifierMetadataRetriever,
    LinearRegressionMetadataRetriever,
    LogisticRegressionMetadataRetriever,
    MetadataRetriever,
    MLPMetadataRetriever,
)


def load_models(paths) -> list:
    models = []
    for path in paths:
        path_obj = Path(path)
        if path_obj.suffix in {".pt", ".pth"}:
            models.append(load_torch_state_dict(path_obj))
        else:
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
    elif isinstance(util_model, nn.Module):
        return MLPMetadataRetriever
    else:
        raise ValueError(f"Unsupported model type: {type(util_model)}")


def _load_torch_mlp(path: Path):
    """Load a simple MLP from a PyTorch state dict and return a torch.nn.Module."""
    state = torch.load(path, map_location="cpu")
    if not isinstance(state, (OrderedDict, dict)):
        raise ValueError("Expected a state_dict for MLP torch model")

    # Infer layer order from keys like fc1.weight, fc1.bias, fc2.weight, ...
    weight_keys = sorted([k for k in state.keys() if k.endswith(".weight")])
    bias_keys = [k.replace(".weight", ".bias") for k in weight_keys]
    layers = []
    for idx, (wk, bk) in enumerate(zip(weight_keys, bias_keys)):
        w = state[wk]
        b = state[bk]
        in_f = w.shape[1]
        out_f = w.shape[0]
        linear = nn.Linear(in_f, out_f)
        linear.weight.data.copy_(w)
        linear.bias.data.copy_(b)
        layers.append(linear)
        # Add ReLU after all but final linear
        if idx < len(weight_keys) - 1:
            layers.append(nn.ReLU())

    model = nn.Sequential(*layers)
    model.eval()
    return model


def load_torch_state_dict(path: Path):
    """Public helper for loading torch state_dict MLPs."""
    return _load_torch_mlp(path)
