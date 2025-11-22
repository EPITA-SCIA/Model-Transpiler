    // Input array sized from model metadata
    real input_v[0:MAX_LAYER_SIZE-1];
    integer parsed_args;
    reg [8*64-1:0] program_name;
    integer i;
    integer n_input;
    integer n_output;
    initial begin
        n_input = layer_sizes[0];
        n_output = layer_sizes[n_layers];

        // Initialize inputs to zero
        for (i = 0; i < n_input; i = i + 1)
            input_v[i] = 0.0;

        parse_positional_args(n_input, parsed_args, program_name);
        if (parsed_args != n_input) begin
            $display("Usage: %0s <feature1> <feature2> ... <featureN>", program_name);
            $finish(1);
        end

        // Preprocessing (in-place)
        preprocessing(n_input);

        // Forward pass
        mlp();

        $write("Prediction:");
        for (i = 0; i < n_output; i = i + 1)
            $write(" %f", mlp_out[i]);
        $write("\n");
        $finish;
    end
