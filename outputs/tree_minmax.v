module main;
integer n_classes = 3;
reg [8*4-1:0] classes[0:2];
initial begin
classes[0] = "-1";
classes[1] = "0";
classes[2] = "1";
end
integer n_input = 3;
integer n_features = 25;
reg integer features[0:24];
initial begin
features[0] = 2;
features[1] = 0;
features[2] = -2;
features[3] = 1;
features[4] = -2;
features[5] = 0;
features[6] = 0;
features[7] = -2;
features[8] = -2;
features[9] = 0;
features[10] = -2;
features[11] = 0;
features[12] = -2;
features[13] = -2;
features[14] = 1;
features[15] = 0;
features[16] = -2;
features[17] = -2;
features[18] = 0;
features[19] = -2;
features[20] = 0;
features[21] = 0;
features[22] = -2;
features[23] = -2;
features[24] = -2;
end
reg real thresholds[0:24];
initial begin
thresholds[0] = 0.5;
thresholds[1] = 0.03095395490527153;
thresholds[2] = -2.0;
thresholds[3] = 0.75;
thresholds[4] = -2.0;
thresholds[5] = 0.3421917259693146;
thresholds[6] = 0.25795799493789673;
thresholds[7] = -2.0;
thresholds[8] = -2.0;
thresholds[9] = 0.4839934706687927;
thresholds[10] = -2.0;
thresholds[11] = 0.552770346403122;
thresholds[12] = -2.0;
thresholds[13] = -2.0;
thresholds[14] = 0.25;
thresholds[15] = 0.6974984705448151;
thresholds[16] = -2.0;
thresholds[17] = -2.0;
thresholds[18] = 0.085538599640131;
thresholds[19] = -2.0;
thresholds[20] = 0.37814177572727203;
thresholds[21] = 0.3188788592815399;
thresholds[22] = -2.0;
thresholds[23] = -2.0;
thresholds[24] = -2.0;
end
reg integer children_left[0:24];
initial begin
children_left[0] = 1;
children_left[1] = 2;
children_left[2] = -1;
children_left[3] = 4;
children_left[4] = -1;
children_left[5] = 6;
children_left[6] = 7;
children_left[7] = -1;
children_left[8] = -1;
children_left[9] = 10;
children_left[10] = -1;
children_left[11] = 12;
children_left[12] = -1;
children_left[13] = -1;
children_left[14] = 15;
children_left[15] = 16;
children_left[16] = -1;
children_left[17] = -1;
children_left[18] = 19;
children_left[19] = -1;
children_left[20] = 21;
children_left[21] = 22;
children_left[22] = -1;
children_left[23] = -1;
children_left[24] = -1;
end
reg integer children_right[0:24];
initial begin
children_right[0] = 14;
children_right[1] = 3;
children_right[2] = -1;
children_right[3] = 5;
children_right[4] = -1;
children_right[5] = 9;
children_right[6] = 8;
children_right[7] = -1;
children_right[8] = -1;
children_right[9] = 11;
children_right[10] = -1;
children_right[11] = 13;
children_right[12] = -1;
children_right[13] = -1;
children_right[14] = 18;
children_right[15] = 17;
children_right[16] = -1;
children_right[17] = -1;
children_right[18] = 20;
children_right[19] = -1;
children_right[20] = 24;
children_right[21] = 23;
children_right[22] = -1;
children_right[23] = -1;
children_right[24] = -1;
end
reg real values[0:24][0:2];
initial begin
values[0][0] = 0.075;
values[0][1] = 0.375;
values[0][2] = 0.55;
values[1][0] = 0.14285714285714285;
values[1][1] = 0.7857142857142857;
values[1][2] = 0.07142857142857142;
values[2][0] = 1.0;
values[2][1] = 0.0;
values[2][2] = 0.0;
values[3][0] = 0.07692307692307693;
values[3][1] = 0.8461538461538461;
values[3][2] = 0.07692307692307693;
values[4][0] = 0.0;
values[4][1] = 1.0;
values[4][2] = 0.0;
values[5][0] = 0.125;
values[5][1] = 0.75;
values[5][2] = 0.125;
values[6][0] = 0.0;
values[6][1] = 0.6666666666666666;
values[6][2] = 0.3333333333333333;
values[7][0] = 0.0;
values[7][1] = 1.0;
values[7][2] = 0.0;
values[8][0] = 0.0;
values[8][1] = 0.0;
values[8][2] = 1.0;
values[9][0] = 0.2;
values[9][1] = 0.8;
values[9][2] = 0.0;
values[10][0] = 0.0;
values[10][1] = 1.0;
values[10][2] = 0.0;
values[11][0] = 0.3333333333333333;
values[11][1] = 0.6666666666666666;
values[11][2] = 0.0;
values[12][0] = 1.0;
values[12][1] = 0.0;
values[12][2] = 0.0;
values[13][0] = 0.0;
values[13][1] = 1.0;
values[13][2] = 0.0;
values[14][0] = 0.038461538461538464;
values[14][1] = 0.15384615384615385;
values[14][2] = 0.8076923076923077;
values[15][0] = 0.0;
values[15][1] = 0.5;
values[15][2] = 0.5;
values[16][0] = 0.0;
values[16][1] = 0.0;
values[16][2] = 1.0;
values[17][0] = 0.0;
values[17][1] = 1.0;
values[17][2] = 0.0;
values[18][0] = 0.05;
values[18][1] = 0.05;
values[18][2] = 0.9;
values[19][0] = 0.0;
values[19][1] = 1.0;
values[19][2] = 0.0;
values[20][0] = 0.05263157894736842;
values[20][1] = 0.0;
values[20][2] = 0.9473684210526315;
values[21][0] = 0.125;
values[21][1] = 0.0;
values[21][2] = 0.875;
values[22][0] = 0.0;
values[22][1] = 0.0;
values[22][2] = 1.0;
values[23][0] = 1.0;
values[23][1] = 0.0;
values[23][2] = 0.0;
values[24][0] = 0.0;
values[24][1] = 0.0;
values[24][2] = 1.0;
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


    // Decision tree classification matching the C helper signature.
    function integer decision_tree;
        input integer dummy; // unused, kept for compatibility
        integer node;
        integer feat;
        real thresh;
        integer max_i;
        real max_val;
        integer i;
        begin
            node = 0;
            while (features[node] != -2) begin
                feat = features[node];
                thresh = thresholds[node];
                if (input_v[feat] <= thresh)
                    node = children_left[node];
                else
                    node = children_right[node];
            end

            max_i = 0;
            max_val = -1.0;
            for (i = 0; i < n_classes; i = i + 1) begin
                if (values[node][i] > max_val) begin
                    max_val = values[node][i];
                    max_i = i;
                end
            end
            decision_tree = max_i;
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

endmodule
