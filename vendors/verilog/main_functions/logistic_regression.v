    // Fixed-size arrays (3 features)
    real input_v[0:2];
    real pred;
    integer max_i;
    real tmp;
    initial begin
        // Initialize inputs
        input_v[0] = 205.9991686803;
        input_v[1] = 2.0;
        input_v[2] = 0.0;

        // Positional arguments override defaults in order (x0 x1 x2)
        parse_positional_args();

        // Named plusargs override anything earlier
        if ($value$plusargs("x0=%f", tmp)) input_v[0] = tmp;
        if ($value$plusargs("x1=%f", tmp)) input_v[1] = tmp;
        if ($value$plusargs("x2=%f", tmp)) input_v[2] = tmp;
        $display("Input 1: %f", input_v[0]);
        $display("Input 2: %f", input_v[1]);
        $display("Input 3: %f", input_v[2]);

        // Initialize weights
        // Initialize weights (provided by generated metadata)

        // Prediction
        pred = logistic_prediction(0);
        max_i = (pred < 0.5) ? 0 : 1;

        $display("Prediction: %f", pred);
        // Use generated `classes` string array when available
        $display("Predicted class: %s", classes[max_i]);
        $finish;
    end
