    // Fixed-size input array
    real input_v[0:2]; // adjust size as needed
    real pred;
    real tmp;
    initial begin
        // Initialize inputs (default values)
        input_v[0] = 1.0;
        input_v[1] = 2.0;
        input_v[2] = 3.0;

        // Positional arguments override defaults
        parse_positional_args();

        // Named plusargs override anything earlier
        if ($value$plusargs("x0=%f", tmp)) input_v[0] = tmp;
        if ($value$plusargs("x1=%f", tmp)) input_v[1] = tmp;
        if ($value$plusargs("x2=%f", tmp)) input_v[2] = tmp;
        
        $display("Input 1: %f", input_v[0]);
        $display("Input 2: %f", input_v[1]);
        $display("Input 3: %f", input_v[2]);

        // Prediction
        pred = linear_regression(0);

        $display("Prediction: %f", pred);
        $finish;
    end
