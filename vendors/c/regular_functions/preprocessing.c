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
