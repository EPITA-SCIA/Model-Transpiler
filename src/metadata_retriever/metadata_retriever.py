from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from src.metadata_retriever.utils import get_preprocessing_id, get_list, get_matrix, get_string_list
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

    def _retrieve_preprocessing(self) -> dict:
        res = dict()
        if isinstance(self.model, Pipeline):
            for _, step in self.model.steps:
                if isinstance(step, MinMaxScaler):
                    res["preprocessing_type"] = get_preprocessing_id("min_max_scaler")
                    res["data_min"] = get_list(step.data_min_, self.language)
                    res["data_max"] = get_list(step.data_max_, self.language)
                    res["feature_range"] = get_list(step.feature_range, self.language)
                    res["clip"] = str(step.clip).lower()
                    break
            else:
                res["preprocessing_type"] = get_preprocessing_id(None)
        else:
            res["preprocessing_type"] = get_preprocessing_id(None)
        return res

    def _retrieve_model_metadata(self, model) -> dict:
        res = dict()
        if isinstance(model, LogisticRegression):
            res["n_thetas"] = model.coef_.shape[1] + 1  # +1 for intercept
            res["n_classes"] = len(model.classes_)
            res["classes"] = get_string_list(model.classes_, self.language)
            if len(model.classes_) == 2:
                res["thetas"] = get_list(model.intercept_.tolist() + model.coef_[0].tolist(), self.language)
            else:
                coefs = model.coef_.tolist()
                for i, intercept in enumerate(model.intercept_):
                    coefs[i] = [intercept] + coefs[i]
                res["thetas"] = get_matrix(coefs, self.language)
        elif isinstance(model, LinearRegression):
            res["n_thetas"] = model.coef_.shape[0] + 1  # +1 for intercept
            res["thetas"] = get_list([model.intercept_] + model.coef_.tolist(), self.language)
        elif isinstance(model, DecisionTreeClassifier):
            res["n_classes"] = len(model.classes_)
            res["classes"] = get_string_list(model.classes_, self.language)
            res["n_input"] = model.n_features_in_
            res["n_features"] = len(model.tree_.feature)
            res["features"] = get_list(model.tree_.feature, self.language)
            res["thresholds"] = get_list(model.tree_.threshold, self.language)
            res["children_left"] = get_list(model.tree_.children_left, self.language)
            res["children_right"] = get_list(model.tree_.children_right, self.language)
            res["values"] = get_matrix(np.squeeze(model.tree_.value), self.language)
        else:
            raise ValueError(f"Unsupported model type: {type(model)}")
        return res

    def retrieve_metadata(self) -> dict:
        preprocessing_metadata = self._retrieve_preprocessing()
        model_metadata = self._retrieve_model_metadata(self._get_model())
        return dict(model_metadata, **preprocessing_metadata)