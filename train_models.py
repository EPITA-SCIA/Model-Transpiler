import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import joblib

df = pd.read_csv(Path(__file__).parent / "houses.csv")


def build_linear_model():
    X = df[["size", "nb_rooms", "garden"]]
    y = df["price"]
    model = LinearRegression()
    model.fit(X, y)
    joblib.dump(model, "linear.joblib")


def build_binary_classes_logistic_model():
    X = df[["size", "nb_rooms", "garden"]]
    y = df["price"] < 270000
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, "logistic_binary.joblib")


def build_multi_classes_logistic_model():
    X = df[["size", "nb_rooms", "garden"]]
    y = np.where(df["price"] < 0, -1, np.where(df["price"] < 270000, 0, 1))
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, "logistic_multi.joblib")


def build_decision_tree_model():
    X = df[["size", "nb_rooms", "garden"]]
    # y = df["price"] < 270000
    y = np.where(df["price"] < 0, -1, np.where(df["price"] < 270000, 0, 1))
    model = DecisionTreeClassifier()
    model.fit(X, y)
    joblib.dump(model, "tree.joblib")
