module main;
integer n_thetas = 4;
reg real thetas[0:3];
initial begin
thetas[0] = 80956.42973354438;
thetas[1] = 118337.44492313299;
thetas[2] = 73648.3919485127;
thetas[3] = 101571.84002157043;
end
integer preprocessing_type = 1;
reg real data_min[0:2];
initial begin
data_min[0] = 72.8958680407;
data_min[1] = 1.0;
data_min[2] = 0.0;
end
reg real data_max[0:2];
initial begin
data_max[0] = 237.8816666324;
data_max[1] = 3.0;
data_max[2] = 1.0;
end
reg real feature_range[0:1];
initial begin
feature_range[0] = 0;
feature_range[1] = 1;
end
integer clip = 0;

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

        // Preprocessing (in-place on input_v)
        preprocessing(expected_args);

        pred = linear_regression(0, n_thetas);

        $display("Prediction: %f", pred);
        $finish;
    end

endmodule
