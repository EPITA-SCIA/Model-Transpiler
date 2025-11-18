double logistic_regression(double* input, double* thetas, int n_parameters){
    return sigmoid(linear_regression(input, thetas, n_parameters));
}