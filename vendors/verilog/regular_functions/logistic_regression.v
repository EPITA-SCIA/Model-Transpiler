    // Logistic regression probability for a given theta vector
    function real logistic_regression;
        input integer theta_idx;
        input integer n_parameters;
        begin
            logistic_regression = sigmoid(logistic_linear_regression(theta_idx, n_parameters));
        end
    endfunction

    // Convenience wrapper using the first theta vector by default
    function real logistic_prediction;
        input integer dummy;
        begin
            logistic_prediction = logistic_regression(0, n_thetas);
        end
    endfunction
