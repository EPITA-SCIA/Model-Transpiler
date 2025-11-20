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