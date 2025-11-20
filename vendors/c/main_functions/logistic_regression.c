/*
int n_classes = 2;
int n_thetas = 4;
double thetas[4] = {2.1835375182032752,0.0015311924364074755,-0.5030500981617257,-2.3800354562177355};
char* classes[2] = {"False","True"};
------
int n_classes = 3;
int n_thetas = 4;
double thetas[3][4] = {{0.8519075687098803,-0.009029285666265086,-0.17786050695273753,-0.55352977035636},{0.7941954819838268,0.007277051080075089,-0.28753355968349126,-1.3190689192239167},{-1.6461030506936434,0.0017522345862986852,0.46539406663648886,1.8725986895831817}};
char* classes[3] = {"-1","0","1"};
*/

void main(int argc, char** argv){
    if (argc != n_thetas) {
        printf("Usage: %s <feature1> <feature2> ... <featureN>\n", argv[0]);
        return;
    }
    
    double inputs[n_thetas - 1];
    for (int i = 1; i < n_thetas; i++) {
        inputs[i-1] = atof(argv[i]);
    }

    if (n_classes == 2) {
        double pred = logistic_regression(inputs, thetas, n_thetas);
    
        int max_i = pred < 0.5 ? 0 : 1;
    
        printf("Prediction: %f\n", pred);
        printf("Predicted class: %s\n", classes[max_i]);
    }
    else {
        int max_i = 0;
        double max = -1;

        for (int i = 0; i < n_classes; i++) {
            double pred = logistic_regression_prediction(inputs, thetas[i], n_parameters);
            if (pred > max) {
                max = pred;
                max_i = i;
            }
        }
    }
}