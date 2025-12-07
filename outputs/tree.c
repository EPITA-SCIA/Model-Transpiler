
# include <stdio.h>
# include <stdlib.h>
# include <stdbool.h>


int n_classes = 3;
char *classes[3] = {"-1", "0", "1"};
int n_input = 3;
int n_features = 23;
int features[23] = {2, 0, -2, 0, 0, 0, -2, 0, -2, -2, -2, -2, 1, 0, -2, -2, 0, -2, 0, 0, -2, -2, -2};
double thresholds[23] = {0.5, 78.0028305053711, -2.0, 164.09512329101562, 152.74791717529297, 115.45527648925781, -2.0, 121.5331802368164, -2.0, -2.0, -2.0, -2.0, 1.5, 187.97321319580078, -2.0, -2.0, 87.0085220336914, -2.0, 135.2838897705078, 125.50635147094727, -2.0, -2.0, -2.0};
int children_left[23] = {1, 2, -1, 4, 5, 6, -1, 8, -1, -1, -1, -1, 13, 14, -1, -1, 17, -1, 19, 20, -1, -1, -1};
int children_right[23] = {12, 3, -1, 11, 10, 7, -1, 9, -1, -1, -1, -1, 16, 15, -1, -1, 18, -1, 22, 21, -1, -1, -1};
double values[23][3] = {{0.075, 0.375, 0.55}, {0.14285714285714285, 0.7857142857142857, 0.07142857142857142}, {1.0, 0.0, 0.0}, {0.07692307692307693, 0.8461538461538461, 0.07692307692307693}, {0.125, 0.75, 0.125}, {0.0, 0.8571428571428571, 0.14285714285714285}, {0.0, 1.0, 0.0}, {0.0, 0.75, 0.25}, {0.0, 0.0, 1.0}, {0.0, 1.0, 0.0}, {1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, {0.038461538461538464, 0.15384615384615385, 0.8076923076923077}, {0.0, 0.5, 0.5}, {0.0, 0.0, 1.0}, {0.0, 1.0, 0.0}, {0.05, 0.05, 0.9}, {0.0, 1.0, 0.0}, {0.05263157894736842, 0.0, 0.9473684210526315}, {0.125, 0.0, 0.875}, {0.0, 0.0, 1.0}, {1.0, 0.0, 0.0}, {0.0, 0.0, 1.0}};
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


int decision_tree(int n_features, int n_classes, double *input, int *features, double *treshold, int *children_left, int *children_right, double (*values)[n_classes])
{
    int node = 0;
    while (features[node] != -2)
    {
        int feat = features[node];
        double tresh = treshold[node];
        if (input[feat] <= tresh)
            node = children_left[node];
        else
            node = children_right[node];
    }
    int max_i = 0;
    double max = -1;
    for (int i = 0; i < n_classes; i++)
    {
        if (values[node][i] > max)
        {
            max = values[node][i];
            max_i = i;
        }
    }
    return max_i;
}

int main(int argc, char** argv){
    if (argc != n_input + 1){
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return 1;
    }
    
    double inputs[n_input];
    for (int i = 1; i < n_input + 1; i++){
        inputs[i-1] = atof(argv[i]);
    }

    preprocessing(inputs, n_input);

    int pred = decision_tree(n_features, n_classes, inputs, features, thresholds, children_left, children_right, values);

    printf("Predicted class: %s\n", classes[pred]);
    return 0;
}

