    parameter integer MAX_INPUTS = 64; // buffer size for inputs
    // Inputs mirror the C main: expects n_input feature values
    real input_v[0:MAX_INPUTS-1];
    integer pred;
    integer parsed_args;
    reg [8*64-1:0] program_name;
    integer i;
    initial begin
        if (n_input > MAX_INPUTS) begin
            $display("Configured feature count (%0d) exceeds MAX_INPUTS buffer", n_input);
            $finish(1);
        end

        for (i = 0; i < n_input; i = i + 1)
            input_v[i] = 0.0;

        parse_positional_args(n_input, parsed_args, program_name);
        if (parsed_args != n_input) begin
            $display("Usage: %0s <feature1> <feature2> ... <featureN>", program_name);
            $finish(1);
        end

        // Preprocessing (in-place on input_v)
        preprocessing(n_input);

        pred = decision_tree(0);

        $display("Predicted class: %s", classes[pred]);
        $finish;
    end
