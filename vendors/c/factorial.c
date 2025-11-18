double factorial(int a){
    double res = 1;
    while (a > 0){
        res *= a;
        a--;
    }
    return res;
}