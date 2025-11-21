int main(int argc, char** argv){
    if (argc != n_thetas){
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return 1;
    }
    
    double inputs[n_thetas - 1];
    for (int i = 1; i < n_thetas; i++){
        inputs[i-1] = atof(argv[i]);
    }

    preprocessing(inputs, n_thetas - 1);

    printf("Prediction: %f\n", linear_regression(inputs, thetas, n_thetas));
    return 0;
}
