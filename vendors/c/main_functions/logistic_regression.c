int main(int argc, char** argv){
    if (argc != n_thetas) {
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return 1;
    }
    
    double inputs[n_thetas - 1];
    for (int i = 1; i < n_thetas; i++) {
        inputs[i-1] = atof(argv[i]);
    }

    preprocessing(inputs, n_thetas - 1);

    if (n_classes == 2) {
        double pred = logistic_regression(inputs, thetas[0], n_thetas);
    
        int max_i = pred < 0.5 ? 0 : 1;
    
        printf("Prediction: %f\n", pred);
        printf("Predicted class: %s\n", classes[max_i]);
    }
    else {
        int max_i = 0;
        double max = -1;

        for (int i = 0; i < n_classes; i++) {
            double pred = logistic_regression(inputs, thetas[i], n_thetas);
            if (pred > max) {
                max = pred;
                max_i = i;
            }
        }
        printf("Prediction: %f\n", max);
        printf("Predicted class: %s\n", classes[max_i]);
    }
    return 0;
}
