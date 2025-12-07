
# include <stdio.h>
# include <stdlib.h>
# include <stdbool.h>


int n_thetas = 4;
int n_classes = 3;
char *classes[3] = {"-1", "0", "1"};
double thetas[3][4] = {{0.8519075687098803, -0.009029285666265086, -0.17786050695273753, -0.55352977035636}, {0.7941954819838268, 0.007277051080075089, -0.28753355968349126, -1.3190689192239167}, {-1.6461030506936434, 0.0017522345862986852, 0.46539406663648886, 1.8725986895831817}};
int preprocessing_type = 0;
double data_min[3] = {0.0, 0.0, 0.0};
double data_max[3] = {1.0, 1.0, 1.0};
double feature_range[2] = {0.0, 1.0};
bool clip = false;

double factorial(int a){
    double res = 1;
    while (a > 0){
        res *= a;
        a--;
    }
    return res;
}

double pow(double a, int b) {
    double res = 1;
    for (int i = 0; i < b; i++){
        res *= a;
    }
    return res;
}

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

double sigmoid(double x){
    return 1 / (1 + exp_approx(-x, 10));
}

void preprocessing(double* input, int n_features){
    if (preprocessing_type == 0){
        return; // no preprocessing
    }
    else if (preprocessing_type == 1){
        // MinMaxScaler: feature_range[0] + (input - data_min)/(data_max - data_min) * (feature_range[1]-feature_range[0])
        double range_min = feature_range[0];
        double range_max = feature_range[1];
        for (int i = 0; i < n_features; i++){
            double denom = data_max[i] - data_min[i];
            double scaled = 0.0;
            if (denom != 0){
                scaled = (input[i] - data_min[i]) / denom;
            }
            // When denom is zero, sklearn MinMaxScaler sets scale to 0 -> output range_min
            double val = range_min + scaled * (range_max - range_min);
            if (clip){
                if (val < range_min) val = range_min;
                else if (val > range_max) val = range_max;
            }
            input[i] = val;
        }
    }
}


double linear_regression(double* input, double* thetas, int n_parameters){
    double res = thetas[0];
    for (int i = 0; i < n_parameters - 1; i++){
        res += input[i] * thetas[i+1];
    }
    return res;
}

double logistic_regression(double* input, double* thetas, int n_parameters){
    return sigmoid(linear_regression(input, thetas, n_parameters));
}

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

