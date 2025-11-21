    // Linear regression mirroring the C helper:
    //   double linear_regression(double* input, double* thetas, int n_parameters)
    // Inputs are taken from the global `input_v` array; only a single theta vector exists in this context.
    function real linear_regression;
        input integer theta_idx_unused; // kept for compatibility with callers
        input integer n_parameters;     // number of parameters (bias + features)
        integer i;
        real res;
        begin
            res = thetas[0];
            for (i = 0; i < n_parameters - 1; i = i + 1)
                res = res + input_v[i] * thetas[i+1];
            linear_regression = res;
        end
    endfunction

    // Legacy wrapper used by linear-only flows
    function real linear_prediction;
        input integer dummy;
        begin
            linear_prediction = linear_regression(0, n_thetas);
        end
    endfunction
