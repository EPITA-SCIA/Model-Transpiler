/*
int n_thetas = 4;
double thetas[4] = {2.1835375182032752,0.0015311924364074755,-0.5030500981617257,-2.3800354562177355};
*/

void main(int argc, char** argv){
    if (argc != n_thetas){
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return;
    }
    
    double inputs[n_thetas - 1];
    for (int i = 1; i < n_thetas; i++){
        inputs[i-1] = atof(argv[i]);
    }

    printf("Prediction: %f\n", linear_regression(inputs, thetas, n_thetas));
}