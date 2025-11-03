import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from . import c_functions

df = pd.read_csv(Path(__file__).parent / "../houses.csv")


def linear_model_to_c(model: LinearRegression, input, verbose, output="linear_model.c"):
    if verbose:
        input_df = pd.DataFrame([input], columns=model.feature_names_in_)
        print("=========== Linear Model ===========")
        print(f"Data = {input}")
        print(f"Prediction = {model.predict(input_df)}")
        print()
    c_code = f"""
    #include <stdio.h>
          
    {c_functions.linear_regression()}
    
    {c_functions.linear_regression_main(model=model, input=input)}    
    """

    with open(output, "w") as text_file:
        text_file.write(c_code)


def logistic_model_to_c(
    model: LogisticRegression, input, verbose, output="logistic_model.c"
):
    if verbose:
        input_df = pd.DataFrame([input], columns=model.feature_names_in_)
        print("=========== Logistic Model ===========")
        print(f"Data = {input}")
        print(f"Prediction = {model.predict(input_df)}")
        print(f"Prediction probabilities = {model.predict_proba(input_df)}")
        print()
    main_func = (
        c_functions.multiclasses_logistic_regression_main
        if len(model.classes_) > 2
        else c_functions.binary_logistic_regression_main
    )

    c_code = f"""
    #include <stdio.h>
    
    {c_functions.pow()}
    
    {c_functions.factorial()}
    
    {c_functions.exp_aprox()}
          
    {c_functions.sigmoid()}

    {c_functions.linear_regression()}
          
    {c_functions.logistic_regression()}
    
    {main_func(model=model, input=input)}
    """

    with open(output, "w") as text_file:
        text_file.write(c_code)


def decision_tree_model_to_c(
    model: DecisionTreeClassifier, input, verbose, output="decision_tree_model.c"
):
    if verbose:
        input_df = pd.DataFrame([input], columns=model.feature_names_in_)
        print("=========== Decision Tree Model ===========")
        print(f"Data = {input}")
        print(f"Prediction = {model.predict(input_df)}")
        print(f"Prediction probabilities = {model.predict_proba(input_df)}")
        print()
    c_code = f"""
    #include <stdio.h>

    {c_functions.decision_tree_classifier()}

    {c_functions.decision_tree_classifier_main(model, input)}
    """

    with open(output, "w") as text_file:
        text_file.write(c_code)


def transpile(model, input, verbose=False, output=None):
    extra_args = {"output": output} if output is not None else {}

    if isinstance(model, LogisticRegression):
        logistic_model_to_c(model=model, input=input, verbose=verbose, **extra_args)
    elif isinstance(model, LinearRegression):
        linear_model_to_c(model=model, input=input, verbose=verbose, **extra_args)
    elif isinstance(model, DecisionTreeClassifier):
        decision_tree_model_to_c(
            model=model, input=input, verbose=verbose, **extra_args
        )
    else:
        raise RuntimeError(f"Model of type {type(model)} is unknown.")
