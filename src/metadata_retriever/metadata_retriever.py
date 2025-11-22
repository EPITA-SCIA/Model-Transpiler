import numpy as np
import torch.nn as nn
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from src.metadata_retriever.utils import (
    get_bool_definition,
    get_double_list_definition,
    get_double_matrix_definition,
    get_double_tensor3_definition,
    get_int_definition,
    get_int_list_definition,
    get_preprocessing_id,
    get_string_list_definition,
)


class MetadataRetriever:
    __slots__ = ("model", "language", "model_name")

    def __init__(self, model, language: str):
        self.model = model
        self.language = language
        self.model_name = None  # should be overwritten in subclasses

    def _get_model(self):
        if isinstance(self.model, Pipeline):
            for _, step in self.model.steps:
                if isinstance(
                    step, (LogisticRegression, LinearRegression, DecisionTreeClassifier)
                ):
                    return step
            raise ValueError("No estimator found in the pipeline.")
        else:
            return self.model

    def _retrieve_preprocessing(self) -> list:
        res = []
        target_model = self._get_model()
        n_features = getattr(target_model, "n_features_in_", 1)

        preprocessing_id = get_preprocessing_id(None)
        data_min = [0.0] * n_features
        data_max = [1.0] * n_features
        feature_range = [0.0, 1.0]
        clip_val = False

        if isinstance(self.model, Pipeline):
            for _, step in self.model.steps:
                if isinstance(step, MinMaxScaler):
                    preprocessing_id = get_preprocessing_id("min_max_scaler")
                    data_min = step.data_min_.tolist()
                    data_max = step.data_max_.tolist()
                    feature_range = list(step.feature_range)
                    clip_val = bool(step.clip)
                    break

        res.append(
            get_int_definition("preprocessing_type", preprocessing_id, self.language)
        )
        res.append(get_double_list_definition("data_min", data_min, self.language))
        res.append(get_double_list_definition("data_max", data_max, self.language))
        res.append(
            get_double_list_definition("feature_range", feature_range, self.language)
        )
        res.append(get_bool_definition("clip", clip_val, self.language))
        return res

    def _retrieve_model_metadata(self, model) -> list:
        raise ValueError("This method should be overwritten.")

    def retrieve_metadata(self) -> list:
        preprocessing_metadata = self._retrieve_preprocessing()
        model_metadata = self._retrieve_model_metadata(self._get_model())
        model_metadata.extend(preprocessing_metadata)
        return model_metadata, self.model_name


class LinearRegressionMetadataRetriever(MetadataRetriever):
    def __init__(self, model, language: str):
        super().__init__(model, language)
        if not isinstance(self._get_model(), LinearRegression):
            raise ValueError("Model must be an instance of LinearRegression.")
        self.model_name = "linear_regression"

    def _retrieve_model_metadata(self, model) -> list:
        res = []
        res.append(
            get_int_definition("n_thetas", model.coef_.shape[0] + 1, self.language)
        )  # +1 for intercept
        res.append(
            get_double_list_definition(
                "thetas", [model.intercept_] + model.coef_.tolist(), self.language
            )
        )

        return res


class LogisticRegressionMetadataRetriever(MetadataRetriever):
    def __init__(self, model, language: str):
        super().__init__(model, language)
        if not isinstance(self._get_model(), LogisticRegression):
            raise ValueError("Model must be an instance of LogisticRegression.")
        self.model_name = "logistic_regression"

    def _retrieve_model_metadata(self, model) -> list:
        res = []
        res.append(
            get_int_definition("n_thetas", model.coef_.shape[1] + 1, self.language)
        )  # +1 for intercept
        res.append(get_int_definition("n_classes", len(model.classes_), self.language))
        res.append(get_string_list_definition("classes", model.classes_, self.language))
        if len(model.classes_) == 2:
            res.append(
                get_double_matrix_definition(
                    "thetas",
                    [model.intercept_.tolist() + model.coef_[0].tolist()],
                    self.language,
                )
            )
        else:
            coefs = model.coef_.tolist()
            for i, intercept in enumerate(model.intercept_):
                coefs[i] = [intercept] + coefs[i]
            res.append(get_double_matrix_definition("thetas", coefs, self.language))

        return res


class DecisionTreeClassifierMetadataRetriever(MetadataRetriever):
    def __init__(self, model, language: str):
        super().__init__(model, language)
        if not isinstance(self._get_model(), DecisionTreeClassifier):
            raise ValueError("Model must be an instance of DecisionTreeClassifier.")
        self.model_name = "decision_tree"

    def _retrieve_model_metadata(self, model) -> list:
        res = []
        res.append(get_int_definition("n_classes", len(model.classes_), self.language))
        res.append(get_string_list_definition("classes", model.classes_, self.language))
        res.append(get_int_definition("n_input", model.n_features_in_, self.language))
        res.append(
            get_int_definition("n_features", len(model.tree_.feature), self.language)
        )
        res.append(
            get_int_list_definition("features", model.tree_.feature, self.language)
        )
        res.append(
            get_double_list_definition(
                "thresholds", model.tree_.threshold, self.language
            )
        )
        res.append(
            get_int_list_definition(
                "children_left", model.tree_.children_left, self.language
            )
        )
        res.append(
            get_int_list_definition(
                "children_right", model.tree_.children_right, self.language
            )
        )
        res.append(
            get_double_matrix_definition(
                "values", np.squeeze(model.tree_.value), self.language
            )
        )

        return res


class MLPMetadataRetriever(MetadataRetriever):
    def __init__(self, model, language):
        super().__init__(model, language)
        self.model_name = "mlp"

    def _get_model(self):
        return self.model

    def _retrieve_preprocessing(self) -> list:
        # Use base preprocessing handling (e.g., MinMaxScaler in a pipeline or defaults)
        return super()._retrieve_preprocessing()

    def _retrieve_model_metadata(self, model) -> list:
        # Flatten supported modules (Linear with optional following ReLU)
        modules = []
        if isinstance(model, nn.Sequential):
            modules = list(model)
        else:
            modules = list(model.children())
            if not modules and isinstance(model, nn.Module):
                # If the module wraps its layers in attributes (not children), fall back to modules()
                modules = [m for m in model.modules() if m is not model][0:]

        weights = []
        biases = []
        activations = []  # 0: linear, 1: relu
        layer_sizes = []

        idx = 0
        while idx < len(modules):
            mod = modules[idx]
            if isinstance(mod, nn.Flatten):
                idx += 1
                continue
            if not isinstance(mod, nn.Linear):
                raise ValueError(f"Unsupported layer type in MLP: {type(mod)}")

            in_features = mod.in_features
            out_features = mod.out_features

            if not layer_sizes:
                layer_sizes.append(in_features)
            elif layer_sizes[-1] != in_features:
                raise ValueError(
                    f"Inconsistent layer sizes: expected {layer_sizes[-1]}, got {in_features}"
                )
            layer_sizes.append(out_features)

            weight = mod.weight.detach().cpu().numpy().tolist()
            bias = mod.bias.detach().cpu().numpy().tolist()

            act = 0
            if idx + 1 < len(modules) and isinstance(modules[idx + 1], nn.ReLU):
                act = 1
                idx += 1  # consume activation

            weights.append(weight)
            biases.append(bias)
            activations.append(act)
            idx += 1

        n_layers = len(weights)
        if n_layers == 0:
            raise ValueError("No Linear layers found in MLP model.")

        max_layer_size = max(layer_sizes)

        # Pad weights/biases to dense tensors [n_layers][max][max] and [n_layers][max]
        padded_weights = []
        padded_biases = []
        for l in range(n_layers):
            in_dim = len(weights[l][0])
            out_dim = len(weights[l])
            padded_w = [
                [0.0 for _ in range(max_layer_size)] for _ in range(max_layer_size)
            ]
            for o in range(out_dim):
                for i in range(in_dim):
                    padded_w[o][i] = weights[l][o][i]
            padded_weights.append(padded_w)

            padded_b = [0.0 for _ in range(max_layer_size)]
            for o in range(out_dim):
                padded_b[o] = biases[l][o]
            padded_biases.append(padded_b)

        res = []
        res.append(get_int_definition("n_layers", n_layers, self.language))
        res.append(get_int_definition("max_layer_size", max_layer_size, self.language))
        if self.language == "verilog":
            res.append(f"localparam integer MAX_LAYER_SIZE = {max_layer_size};")
        res.append(get_int_list_definition("layer_sizes", layer_sizes, self.language))
        res.append(get_int_list_definition("activations", activations, self.language))
        res.append(
            get_double_tensor3_definition("weights", padded_weights, self.language)
        )
        res.append(get_double_matrix_definition("biases", padded_biases, self.language))
        return res
