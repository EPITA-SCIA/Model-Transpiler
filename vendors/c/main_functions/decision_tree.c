void main(int argc, char** argv){
    if (argc != n_input + 1){
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return;
    }
    
    double inputs[n_input];
    for (int i = 1; i < n_input + 1; i++){
        inputs[i-1] = atof(argv[i]);
    }

    int pred = decision_tree(n_features, n_classes, inputs, features, thresholds, children_left, children_right, values);

    printf("Predicted class: %s\n", classes[pred]);
}