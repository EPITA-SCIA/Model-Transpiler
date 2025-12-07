
# include <stdio.h>
# include <stdlib.h>
# include <stdbool.h>


int n_thetas = 4;
double thetas[4] = {-8152.937710156519, 717.2583697096838, 36824.1959742563, 101571.84002157034};
int preprocessing_type = 0;
double data_min[3] = {0.0, 0.0, 0.0};
double data_max[3] = {1.0, 1.0, 1.0};
double feature_range[2] = {0.0, 1.0};
bool clip = false;

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

