    parameter integer MAX_FEATURES = 64; // buffer size for inputs
    // Fixed-size arrays driven by model metadata
    real input_v[0:MAX_FEATURES-1];
    real pred;
    integer max_i;
    real max;
    integer parsed_args;
    reg [8*64-1:0] program_name;
    integer i;
    integer expected_args;
    real cur_pred;
    initial begin
        expected_args = n_thetas - 1;
        if (expected_args > MAX_FEATURES) begin
            $display("Configured feature count (%0d) exceeds MAX_FEATURES buffer", expected_args);
            $finish(1);
        end

        for (i = 0; i < expected_args; i = i + 1)
            input_v[i] = 0.0;

        parse_positional_args(expected_args, parsed_args, program_name);
        if (parsed_args != expected_args) begin
            $display("Usage: %0s <feature1> <feature2> ... <featureN>", program_name);
            $finish(1);
        end

        // Preprocessing (in-place on input_v)
        preprocessing(expected_args);

        if (n_classes == 2) begin
            pred = logistic_regression(0, n_thetas);
            max_i = (pred < 0.5) ? 0 : 1;
            $display("Prediction: %f", pred);
            $display("Predicted class: %s", classes[max_i]);
        end else begin
            max_i = 0;
            max = -1.0;
            for (i = 0; i < n_classes; i = i + 1) begin
                cur_pred = logistic_regression(i, n_thetas);
                if (cur_pred > max) begin
                    max = cur_pred;
                    max_i = i;
                end
            end
            $display("Prediction: %f", max);
            $display("Predicted class: %s", classes[max_i]);
        end
        $finish;
    end
