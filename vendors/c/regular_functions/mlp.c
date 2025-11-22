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
