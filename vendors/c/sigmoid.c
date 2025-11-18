double sigmoid(double x){
    return 1 / (1 + exp_approx(-x, 10));
}