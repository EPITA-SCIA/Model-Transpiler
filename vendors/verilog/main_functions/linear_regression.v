    parameter integer MAX_FEATURES = 64; // buffer size for inputs
    // Inputs mirror the C main: expects n_thetas - 1 feature values
    real input_v[0:MAX_FEATURES-1];
    real pred;
    integer parsed_args;
    reg [8*64-1:0] program_name;
    integer i;
    integer expected_args;
    initial begin
        expected_args = n_thetas - 1;
        if (expected_args > MAX_FEATURES) begin
            $display("Configured feature count (%0d) exceeds MAX_FEATURES buffer", expected_args);
            $finish(1);
        end

        // Clear inputs
        for (i = 0; i < expected_args; i = i + 1)
            input_v[i] = 0.0;

        parse_positional_args(expected_args, parsed_args, program_name);
        if (parsed_args != expected_args) begin
            $display("Usage: %0s <feature1> <feature2> ... <featureN>", program_name);
            $finish(1);
        end

        pred = linear_regression(0, n_thetas);

        $display("Prediction: %f", pred);
        $finish;
    end
