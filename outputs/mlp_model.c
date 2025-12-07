
# include <stdio.h>
# include <stdlib.h>
# include <stdbool.h>


int n_layers = 2;
int max_layer_size = 5;
int layer_sizes[3] = {3, 5, 3};
int activations[2] = {1, 0};
double weights[2][5][5] = {{{-0.3834744393825531, 0.14815139770507812, 0.41372302174568176, 0.0, 0.0}, {-0.37890303134918213, 0.10313352197408676, 0.17588277161121368, 0.0, 0.0}, {-0.4998994767665863, -0.1716492474079132, -0.4076557159423828, 0.0, 0.0}, {0.4440070390701294, 2.0352730751037598, 1.141969084739685, 0.0, 0.0}, {0.04395906999707222, -0.932279646396637, -3.2447261810302734, 0.0, 0.0}}, {{-0.30826830863952637, 0.16870123147964478, -0.1688118577003479, -0.298531711101532, 0.6578521728515625}, {-0.234434574842453, -0.2437085658311844, 0.2678743600845337, -0.27043434977531433, 0.883389949798584}, {0.38831132650375366, 0.15455254912376404, -0.29308515787124634, -0.0968790054321289, -0.9975279569625854}, {0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0}}};
double biases[2][5] = {{-0.04598356410861015, -0.04246073216199875, -0.5501034259796143, -0.3714665174484253, 3.082505464553833}, {2.303253412246704, 0.7141737937927246, -0.7990109920501709, 0.0, 0.0}};
int preprocessing_type = 0;
double data_min[1] = {0.0};
double data_max[1] = {1.0};
double feature_range[2] = {0.0, 1.0};
bool clip = false;

double relu(double x){
    return x > 0 ? x : 0;
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


void mlp(double* input, double* output){
    double buffer_a[max_layer_size];
    double buffer_b[max_layer_size];
    double* current = input;
    double* next = buffer_a;

    for (int l = 0; l < n_layers; l++){
        int in_dim = layer_sizes[l];
        int out_dim = layer_sizes[l + 1];
        for (int o = 0; o < out_dim; o++){
            double sum = biases[l][o];
            for (int i = 0; i < in_dim; i++){
                sum += current[i] * weights[l][o][i];
            }
            if (activations[l] == 1)
                sum = relu(sum);
            next[o] = sum;
        }
        current = next;
        next = (next == buffer_a) ? buffer_b : buffer_a;
    }

    int out_dim = layer_sizes[n_layers];
    for (int o = 0; o < out_dim; o++)
        output[o] = current[o];
}


int main(int argc, char** argv){
    if (argc != layer_sizes[0] + 1){
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return 1;
    }

    int n_input = layer_sizes[0];
    int n_output = layer_sizes[n_layers];

    double inputs[n_input];
    for (int i = 1; i < n_input + 1; i++){
        inputs[i-1] = atof(argv[i]);
    }

    preprocessing(inputs, n_input);

    double outputs[max_layer_size];
    mlp(inputs, outputs);

    printf("Prediction:");
    for (int i = 0; i < n_output; i++){
        printf(" %f", outputs[i]);
    }
    printf("\n");
    return 0;
}
