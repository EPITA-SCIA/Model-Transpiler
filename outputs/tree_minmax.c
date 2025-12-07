
# include <stdio.h>
# include <stdlib.h>
# include <stdbool.h>


int n_classes = 3;
char *classes[3] = {"-1", "0", "1"};
int n_input = 3;
int n_features = 25;
int features[25] = {2, 0, -2, 1, -2, 0, 0, -2, -2, 0, -2, 0, -2, -2, 1, 0, -2, -2, 0, -2, 0, 0, -2, -2, -2};
double thresholds[25] = {0.5, 0.03095395490527153, -2.0, 0.75, -2.0, 0.3421917259693146, 0.25795799493789673, -2.0, -2.0, 0.4839934706687927, -2.0, 0.552770346403122, -2.0, -2.0, 0.25, 0.6974984705448151, -2.0, -2.0, 0.085538599640131, -2.0, 0.37814177572727203, 0.3188788592815399, -2.0, -2.0, -2.0};
int children_left[25] = {1, 2, -1, 4, -1, 6, 7, -1, -1, 10, -1, 12, -1, -1, 15, 16, -1, -1, 19, -1, 21, 22, -1, -1, -1};
int children_right[25] = {14, 3, -1, 5, -1, 9, 8, -1, -1, 11, -1, 13, -1, -1, 18, 17, -1, -1, 20, -1, 24, 23, -1, -1, -1};
double values[25][3] = {{0.075, 0.375, 0.55}, {0.14285714285714285, 0.7857142857142857, 0.07142857142857142}, {1.0, 0.0, 0.0}, {0.07692307692307693, 0.8461538461538461, 0.07692307692307693}, {0.0, 1.0, 0.0}, {0.125, 0.75, 0.125}, {0.0, 0.6666666666666666, 0.3333333333333333}, {0.0, 1.0, 0.0}, {0.0, 0.0, 1.0}, {0.2, 0.8, 0.0}, {0.0, 1.0, 0.0}, {0.3333333333333333, 0.6666666666666666, 0.0}, {1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, {0.038461538461538464, 0.15384615384615385, 0.8076923076923077}, {0.0, 0.5, 0.5}, {0.0, 0.0, 1.0}, {0.0, 1.0, 0.0}, {0.05, 0.05, 0.9}, {0.0, 1.0, 0.0}, {0.05263157894736842, 0.0, 0.9473684210526315}, {0.125, 0.0, 0.875}, {0.0, 0.0, 1.0}, {1.0, 0.0, 0.0}, {0.0, 0.0, 1.0}};
int preprocessing_type = 1;
double data_min[3] = {72.8958680407, 1.0, 0.0};
double data_max[3] = {237.8816666324, 3.0, 1.0};
double feature_range[2] = {0, 1};
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

