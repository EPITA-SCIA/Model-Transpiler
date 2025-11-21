    // Linear component for logistic regression using thetas matrix (one row per class)
    function real logistic_linear_regression;
        input integer theta_idx;
        input integer n_parameters;
        integer i;
        real res;
        begin
            res = thetas[theta_idx][0];
            for (i = 0; i < n_parameters - 1; i = i + 1)
                res = res + input_v[i] * thetas[theta_idx][i+1];
            logistic_linear_regression = res;
        end
    endfunction
