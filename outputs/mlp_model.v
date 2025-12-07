module main;
integer n_layers = 2;
integer max_layer_size = 5;
localparam integer MAX_LAYER_SIZE = 5;
reg integer layer_sizes[0:2];
initial begin
layer_sizes[0] = 3;
layer_sizes[1] = 5;
layer_sizes[2] = 3;
end
reg integer activations[0:1];
initial begin
activations[0] = 1;
activations[1] = 0;
end
reg real weights[0:1][0:4][0:4];
initial begin
weights[0][0][0] = -0.3834744393825531;
weights[0][0][1] = 0.14815139770507812;
weights[0][0][2] = 0.41372302174568176;
weights[0][0][3] = 0.0;
weights[0][0][4] = 0.0;
weights[0][1][0] = -0.37890303134918213;
weights[0][1][1] = 0.10313352197408676;
weights[0][1][2] = 0.17588277161121368;
weights[0][1][3] = 0.0;
weights[0][1][4] = 0.0;
weights[0][2][0] = -0.4998994767665863;
weights[0][2][1] = -0.1716492474079132;
weights[0][2][2] = -0.4076557159423828;
weights[0][2][3] = 0.0;
weights[0][2][4] = 0.0;
weights[0][3][0] = 0.4440070390701294;
weights[0][3][1] = 2.0352730751037598;
weights[0][3][2] = 1.141969084739685;
weights[0][3][3] = 0.0;
weights[0][3][4] = 0.0;
weights[0][4][0] = 0.04395906999707222;
weights[0][4][1] = -0.932279646396637;
weights[0][4][2] = -3.2447261810302734;
weights[0][4][3] = 0.0;
weights[0][4][4] = 0.0;
weights[1][0][0] = -0.30826830863952637;
weights[1][0][1] = 0.16870123147964478;
weights[1][0][2] = -0.1688118577003479;
weights[1][0][3] = -0.298531711101532;
weights[1][0][4] = 0.6578521728515625;
weights[1][1][0] = -0.234434574842453;
weights[1][1][1] = -0.2437085658311844;
weights[1][1][2] = 0.2678743600845337;
weights[1][1][3] = -0.27043434977531433;
weights[1][1][4] = 0.883389949798584;
weights[1][2][0] = 0.38831132650375366;
weights[1][2][1] = 0.15455254912376404;
weights[1][2][2] = -0.29308515787124634;
weights[1][2][3] = -0.0968790054321289;
weights[1][2][4] = -0.9975279569625854;
weights[1][3][0] = 0.0;
weights[1][3][1] = 0.0;
weights[1][3][2] = 0.0;
weights[1][3][3] = 0.0;
weights[1][3][4] = 0.0;
weights[1][4][0] = 0.0;
weights[1][4][1] = 0.0;
weights[1][4][2] = 0.0;
weights[1][4][3] = 0.0;
weights[1][4][4] = 0.0;
end
reg real biases[0:1][0:4];
initial begin
biases[0][0] = -0.04598356410861015;
biases[0][1] = -0.04246073216199875;
biases[0][2] = -0.5501034259796143;
biases[0][3] = -0.3714665174484253;
biases[0][4] = 3.082505464553833;
biases[1][0] = 2.303253412246704;
biases[1][1] = 0.7141737937927246;
biases[1][2] = -0.7990109920501709;
biases[1][3] = 0.0;
biases[1][4] = 0.0;
end
integer preprocessing_type = 0;
reg real data_min[0:0];
initial begin
data_min[0] = 0.0;
end
reg real data_max[0:0];
initial begin
data_max[0] = 1.0;
end
reg real feature_range[0:1];
initial begin
feature_range[0] = 0.0;
feature_range[1] = 1.0;
end
integer clip = 0;

    function real relu;
        input real x;
        begin
            if (x > 0.0)
                relu = x;
            else
                relu = 0.0;
        end
    endfunction


    // Preprocessing function controlled by preprocessing_type:
    // 0: no preprocessing
    // 1: MinMaxScaler using data_min, data_max, feature_range
    task preprocessing;
        input integer n_features;
        integer i;
        real range_min;
        real range_max;
        real denom;
        real scaled;
        begin
            if (preprocessing_type == 0) begin
                // no preprocessing
            end else if (preprocessing_type == 1) begin
                range_min = feature_range[0];
                range_max = feature_range[1];
                for (i = 0; i < n_features; i = i + 1) begin
                    denom = data_max[i] - data_min[i];
                    if (denom != 0.0)
                        scaled = (input_v[i] - data_min[i]) / denom;
                    else
                        scaled = 0.0;
                    input_v[i] = range_min + scaled * (range_max - range_min);
                    if (clip) begin
                        if (input_v[i] < range_min)
                            input_v[i] = range_min;
                        else if (input_v[i] > range_max)
                            input_v[i] = range_max;
                    end
                end
            end
        end
    endtask


    // Simple MLP forward pass with padded weight/bias tensors.
    // Uses global inputs from `input_v` and writes results to `mlp_out`.
    // Global output buffer for MLP inference
    real mlp_out[0:MAX_LAYER_SIZE-1];

    task mlp;
        integer l;
        integer i;
        integer o;
        integer out_dim;
        integer in_dim;
        real buffer_a[0:MAX_LAYER_SIZE-1];
        real buffer_b[0:MAX_LAYER_SIZE-1];
        real tmp;
        reg use_a; // when 0 -> read from buffer_a, when 1 -> read from buffer_b
        begin
            use_a = 1'b0;
            // seed buffer_a with input_v for uniform access
            for (i = 0; i < layer_sizes[0]; i = i + 1)
                buffer_a[i] = input_v[i];

            for (l = 0; l < n_layers; l = l + 1) begin
                in_dim = layer_sizes[l];
                out_dim = layer_sizes[l+1];
                for (o = 0; o < out_dim; o = o + 1) begin
                    tmp = biases[l][o];
                    for (i = 0; i < in_dim; i = i + 1) begin
                        if (use_a)
                            tmp = tmp + buffer_b[i] * weights[l][o][i];
                        else
                            tmp = tmp + buffer_a[i] * weights[l][o][i];
                    end
                    if (activations[l] == 1)
                        tmp = relu(tmp);
                    if (use_a)
                        buffer_a[o] = tmp;
                    else
                        buffer_b[o] = tmp;
                end
                use_a = ~use_a; // swap buffers
            end

            out_dim = layer_sizes[n_layers];
            if (use_a) begin
                for (i = 0; i < out_dim; i = i + 1) mlp_out[i] = buffer_b[i];
            end else begin
                for (i = 0; i < out_dim; i = i + 1) mlp_out[i] = buffer_a[i];
            end
        end
    endtask


    // Parse positional CLI args from /proc/self/cmdline so the simulator can be
    // run as: ./a.out <feature1> <feature2> ... <featureN>
    task parse_positional_args;
        input integer expected_args;
        output integer parsed_count;
        output reg [8*64-1:0] program_name;
        integer fd;
        integer count;
        integer i;
        integer arg_idx;
        integer char_pos;
        reg [7:0] buffer[0:2047];
        reg [8*64-1:0] token;
        real parsed_val;
        integer parsed;
        begin
            parsed_count = 0;
            program_name = "program";
            fd = $fopen("/proc/self/cmdline", "rb");
            if (fd == 0) begin
                $display("Warning: unable to open /proc/self/cmdline; positional args ignored.");
            end else begin

                count = $fread(buffer, fd);
                $fclose(fd);

                arg_idx = -2; // skip interpreter (argv[0]) and design path (argv[1])
                token = {8*64{1'b0}};
                char_pos = 0;

                for (i = 0; i < count; i = i + 1) begin
                    if (buffer[i] == 8'h00) begin
                        if (arg_idx == -1 && char_pos > 0)
                            program_name = token;
                        if (arg_idx >= 0 && char_pos > 0) begin
                            if (parsed_count < expected_args) begin
                                parsed = $sscanf(token, "%f", parsed_val);
                                if (parsed == 1)
                                    input_v[parsed_count] = parsed_val;
                                else
                                    $display("Warning: could not parse positional arg %0d ('%s')", parsed_count + 1, token);
                            end
                            parsed_count = parsed_count + 1;
                        end
                        arg_idx = arg_idx + 1;
                        token = {8*64{1'b0}};
                        char_pos = 0;
                    end else if (arg_idx >= -1 && char_pos < 64) begin
                        token[8*(63-char_pos) +: 8] = buffer[i];
                        char_pos = char_pos + 1;
                    end
                end
            end
        end
    endtask


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

endmodule
