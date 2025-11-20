from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from src.metadata_retriever.utils import (
    get_int_list_definition,
    get_preprocessing_id,
    get_string_list_definition,
    get_double_matrix_definition,
    get_double_list_definition,
    get_int_definition,
    get_bool_definition,
)
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
import numpy as np

class MetadataRetriever():
    def __init__(self, model, language: str):
        self.model = model
        self.language = language

    def _get_model(self):
        if isinstance(self.model, Pipeline):
            for _, step in self.model.steps:
                if isinstance(step, (LogisticRegression, LinearRegression, DecisionTreeClassifier)):
                    return step
            raise ValueError("No estimator found in the pipeline.")
        else:
            return self.model

    def _retrieve_preprocessing(self) -> list:
        res = []
        if isinstance(self.model, Pipeline):
            for _, step in self.model.steps:
                if isinstance(step, MinMaxScaler):
                    res.append(get_preprocessing_id("min_max_scaler"))
                    res.append(get_double_list_definition("data_min", step.data_min_, self.language))
                    res.append(get_double_list_definition("data_max", step.data_max_, self.language))
                    res.append(get_double_list_definition("feature_range", step.feature_range, self.language))
                    res.append(get_bool_definition("clip", step.clip, self.language))
                    break
            else:
                res.append(get_int_definition("preprocessing_type", get_preprocessing_id(None), self.language))
        else:
            res.append(get_int_definition("preprocessing_type", get_preprocessing_id(None), self.language))
        return res

    def _retrieve_model_metadata(self, model) -> list:
        res = []
        model_name = ""
        if isinstance(model, LogisticRegression):
            model_name = "logistic_regression"
            res.append(get_int_definition("n_thetas", model.coef_.shape[1] + 1, self.language))  # +1 for intercept
            res.append(get_int_definition("n_classes", len(model.classes_), self.language))
            res.append(get_string_list_definition("classes", model.classes_, self.language))
            if len(model.classes_) == 2:
                res.append(get_double_list_definition("thetas", model.intercept_.tolist() + model.coef_[0].tolist(), self.language))
            else:
                coefs = model.coef_.tolist()
                for i, intercept in enumerate(model.intercept_):
                    coefs[i] = [intercept] + coefs[i]
                res.append(get_double_matrix_definition("thetas", coefs, self.language))
        elif isinstance(model, LinearRegression):
            model_name = "linear_regression"
            res.append(get_int_definition("n_thetas", model.coef_.shape[0] + 1, self.language))  # +1 for intercept
            res.append(get_double_list_definition("thetas", [model.intercept_] + model.coef_.tolist(), self.language))
        elif isinstance(model, DecisionTreeClassifier):
            model_name = "decision_tree"
            res.append(get_int_definition("n_classes", len(model.classes_), self.language))
            res.append(get_string_list_definition("classes", model.classes_, self.language))
            res.append(get_int_definition("n_input", model.n_features_in_, self.language))
            res.append(get_int_definition("n_features", len(model.tree_.feature), self.language))
            res.append(get_int_list_definition("features", model.tree_.feature, self.language))
            res.append(get_double_list_definition("thresholds", model.tree_.threshold, self.language))
            res.append(get_int_list_definition("children_left", model.tree_.children_left, self.language))
            res.append(get_int_list_definition("children_right", model.tree_.children_right, self.language))
            res.append(get_double_matrix_definition("values", np.squeeze(model.tree_.value), self.language))
        else:
            raise ValueError(f"Unsupported model type: {type(model)}")
        return res, model_name

    def retrieve_metadata(self) -> list:
        preprocessing_metadata = self._retrieve_preprocessing()
        model_metadata, model_name = self._retrieve_model_metadata(self._get_model())
        model_metadata.extend(preprocessing_metadata)
        return model_metadata, model_name
