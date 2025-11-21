    // Preprocessing function controlled by preprocessing_type:
    // 0: no preprocessing
    // 1: MinMaxScaler using data_min, data_max, feature_range
    task preprocessing;
        input integer n_features;
        integer i;
        real range_min;
        real range_max;
        real denom;
        real scaled;
        begin
            if (preprocessing_type == 0) begin
                // no preprocessing
            end else if (preprocessing_type == 1) begin
                range_min = feature_range[0];
                range_max = feature_range[1];
                for (i = 0; i < n_features; i = i + 1) begin
                    denom = data_max[i] - data_min[i];
                    if (denom != 0.0)
                        scaled = (input_v[i] - data_min[i]) / denom;
                    else
                        scaled = 0.0;
                    input_v[i] = range_min + scaled * (range_max - range_min);
                    if (clip) begin
                        if (input_v[i] < range_min)
                            input_v[i] = range_min;
                        else if (input_v[i] > range_max)
                            input_v[i] = range_max;
                    end
                end
            end
        end
    endtask
