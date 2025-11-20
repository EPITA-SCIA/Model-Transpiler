    // Fixed-size input array
    real input_v[0:2]; // adjust size as needed or make generic
    integer pred;
    real tmp;
    initial begin
        // Initialize inputs (default values)
        input_v[0] = 5.1;
        input_v[1] = 3.5;
        input_v[2] = 1.4;

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
        pred = decision_tree(0);

        $display("Predicted class: %s", classes[pred]);
        $finish;
    end
