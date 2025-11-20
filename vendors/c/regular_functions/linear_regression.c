double linear_regression(double* input, double* thetas, int n_parameters){
    double res = thetas[0];
    for (int i = 0; i < n_parameters - 1; i++){
        res += input[i] * thetas[i+1];
    }
    return res;
}