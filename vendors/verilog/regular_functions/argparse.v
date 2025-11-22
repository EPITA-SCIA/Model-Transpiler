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
