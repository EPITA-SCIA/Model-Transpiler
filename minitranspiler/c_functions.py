from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import numpy as np


def list_to_c(python_list: list):
    c_list = "{"
    for i in range(len(python_list)):
        if isinstance(python_list[i], list) or isinstance(python_list[i], np.ndarray):
            c_list += list_to_c(python_list[i])
        else:
            if isinstance(python_list[i], str):
                c_list += f'"{python_list[i]}"'
            else:
                c_list += str(python_list[i])
        if i < len(python_list) - 1:
            c_list += ","
    return c_list + "}"


def linear_regression():
    return """          
double linear_regression_prediction(double* input, double* thetas, int n_parameters){
    double res = thetas[0];
    for (int i = 0; i < n_parameters - 1; i++){
        res += input[i] * thetas[i+1];
    }
    return res;
}"""


def pow():
    return """
double pow(double a, int b) {
    double res = 1;
    for (int i = 0; i < b; i++){
        res *= a;
    }
    return res;
}
"""


def factorial():
    return """
double factorial(int a){
    double res = 1;
    while (a > 0){
        res *= a;
        a--;
    }
    return res;
}
"""


def exp_aprox():
    return """
double exp_approx(double x, int n_term) {
    if (x < 0)
    {
        return 1.0 / exp_approx(-x, n_term);
    }

    double res = 0;
    for (int i = 0; i <= n_term; i++){
        res += pow(x, i) / factorial(i);
    }
    return res;
}
"""


def sigmoid():
    return """
double sigmoid(double x){
    return 1 / (1 + exp_approx(-x, 10));
}
"""


def logistic_regression():
    return """
double logistic_regression_prediction(double* input, double* thetas, int n_parameters){
    return sigmoid(linear_regression_prediction(input, thetas, n_parameters));
}
"""


def decision_tree_classifier():
    return """
int decision_tree_classifier(int n_features, int n_classes, double *input, int *features, double *treshold, int *children_left, int *children_right, double (*values)[n_classes])
{
    int node = 0;
    while (features[node] != -2)
    {
        int feat = features[node];
        double tresh = treshold[node];
        if (input[feat] <= tresh)
            node = children_left[node];
        else
            node = children_right[node];
    }
    int max_i = 0;
    double max = -1;
    for (int i = 0; i < n_classes; i++)
    {
        if (values[node][i] > max)
        {
            max = values[node][i];
            max_i = i;
        }
    }
    return max_i;
}
"""


def multiclasses_logistic_regression_main(model: LogisticRegression, input: list):
    return f"""
void main(){{
    double thetas[{model.coef_.shape[0]}][{model.coef_.shape[1] + 1}] = {list_to_c([[bias, *coefs] for bias, coefs in zip(model.intercept_, model.coef_)])};
    int n_parameters = {len(model.coef_[0]) + 1};
    char* classes[{len(model.classes_)}] = {list_to_c(list(map(str, model.classes_)))};

    double input[{len(input)}] = {{ {", ".join(map(str, input))} }};

    int max_i = 0;
    double max = -1;

    for (int i = 0; i < {model.coef_.shape[0]}; i++)
    {{
        double pred = logistic_regression_prediction(input, thetas[i], n_parameters);
        if (pred > max)
        {{
            max = pred;
            max_i = i;
        }}
    }}

    printf("Predicted class: %s\\n", classes[max_i]);
}}
    """


def binary_logistic_regression_main(model: LogisticRegression, input: list):
    return f"""
void main(){{
    double thetas[{model.coef_.shape[1] + 1}] = {list_to_c([*model.intercept_, *model.coef_[0]])};
    int n_parameters = {model.coef_.shape[1] + 1};
    char* classes[{len(model.classes_)}] = {list_to_c(list(map(str, model.classes_)))};

    double input[{len(input)}] = {{ {", ".join(map(str, input))} }};

    double pred = logistic_regression_prediction(input, thetas, n_parameters);

    int max_i = pred < 0.5 ? 0 : 1;

    printf("Predicted class: %s\\n", classes[max_i]);
}}
    """


def linear_regression_main(model: LinearRegression, input: list):
    return f"""
void main(){{
    double thetas[{len(model.coef_) + 1}] = {{ {", ".join([str(model.intercept_)] + [str(coef) for coef in model.coef_])} }};
    int n_parameters = {len(model.coef_) + 1};

    double input[{len(input)}] = {{ {", ".join(map(str, input))} }};

    printf("Prediction: %f\\n", linear_regression_prediction(input, thetas, n_parameters));
}}"""


def decision_tree_classifier_main(model: DecisionTreeClassifier, input: list):
    return f"""
void main()
{{
    int n_features = {model.tree_.feature.shape[0]};

    int features[{model.tree_.feature.shape[0]}] = {list_to_c(model.tree_.feature)};
    double threshold[{model.tree_.feature.shape[0]}] = {list_to_c(model.tree_.threshold)};
    int children_left[{model.tree_.feature.shape[0]}] = {list_to_c(model.tree_.children_left)};
    int children_right[{model.tree_.feature.shape[0]}] = {list_to_c(model.tree_.children_right)};
    double values[{model.tree_.feature.shape[0]}][{model.tree_.n_classes[0]}] = {list_to_c(np.squeeze(model.tree_.value))};

    int n_classes = {model.tree_.n_classes[0]};
    char *classes[{model.tree_.n_classes[0]}] = {list_to_c(list(map(str, model.classes_)))};

    double input[{len(input)}] = {{ {", ".join(map(str, input))} }};

    int pred = decision_tree_classifier(n_features, n_classes, input, features, threshold, children_left, children_right, values);

    printf("Predicted class: %s\\n", classes[pred]);
}}"""
