    // Linear regression using 1D thetas array (for pure linear regression models)
    // Note: renamed to linear_regression_1d to avoid conflict with logistic_regression.v
    function real linear_regression_1d;
        input integer dummy; // unused, for compatibility
        integer i;
        real res;
        begin
            res = thetas[0];
            for (i = 0; i < n_thetas - 1; i = i + 1)
                res = res + input_v[i] * thetas[i+1];
            linear_regression_1d = res;
        end
    endfunction

    // Main entry point for linear models - calls renamed function
    function real linear_regression;
        input integer dummy;
        begin
            linear_regression = linear_regression_1d(0);
        end
    endfunction

    // Legacy wrapper name
    function real linear_prediction;
        input integer dummy;
        begin
            linear_prediction = linear_regression_1d(0);
        end
    endfunction
