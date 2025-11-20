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