import numpy as np
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier

from src.metadata_retriever.utils import (
    get_bool_definition,
    get_double_list_definition,
    get_double_matrix_definition,
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
        return []

    def _retrieve_model_metadata(self, model) -> list:
        # TODO : implement the function
        pass
