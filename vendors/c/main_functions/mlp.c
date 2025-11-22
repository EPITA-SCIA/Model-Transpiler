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