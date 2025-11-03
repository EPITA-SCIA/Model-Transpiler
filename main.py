from minitranspiler.minitranspiler import transpile
from train_models import (
    build_decision_tree_model,
    build_linear_model,
    build_binary_classes_logistic_model,
    build_multi_classes_logistic_model,
)
import joblib

build_linear_model()
build_binary_classes_logistic_model()
build_multi_classes_logistic_model()
build_decision_tree_model()


input = [205.9991686803, 2, 0]

transpile(model=joblib.load("linear.joblib"), input=input, verbose=True)
transpile(
    model=joblib.load("logistic_binary.joblib"),
    input=input,
    verbose=True,
    output="logistic_binary_model.c",
)
transpile(
    model=joblib.load("logistic_multi.joblib"),
    input=input,
    verbose=True,
    output="logistic_multi_model.c",
)
transpile(model=joblib.load("tree.joblib"), input=input, verbose=True)
