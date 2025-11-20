    // Helper performing per-class linear combination for logistic models
    // Renamed to avoid collision with pure linear regression helpers
    function real logistic_linear_regression;
        input integer class_idx;
        integer i;
        real res;
        begin
            res = thetas(class_idx, 0);
            for (i = 0; i < n_thetas - 1; i = i + 1)
                res = res + input_v[i] * thetas(class_idx, i+1);
            logistic_linear_regression = res;
        end
    endfunction

    // Logistic regression probability for a given class index
    function real logistic_regression;
        input integer class_idx;
        begin
            logistic_regression = sigmoid(logistic_linear_regression(class_idx));
        end
    endfunction

    // Public prediction helper (default class index 0)
    function real logistic_prediction;
        input integer dummy;
        begin
            logistic_prediction = logistic_regression(0);
        end
    endfunction
