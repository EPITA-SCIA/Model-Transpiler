double pow(double a, int b) {
    double res = 1;
    for (int i = 0; i < b; i++){
        res *= a;
    }
    return res;
}