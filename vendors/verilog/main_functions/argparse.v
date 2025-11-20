    // Parse up to three positional CLI args from /proc/self/cmdline so the
    // simulator can be run as: ./a.out <x0> <x1> <x2>
    task automatic parse_positional_args;
        integer fd;
        integer count;
        integer i;
        integer arg_idx;
        integer char_pos;
        reg [7:0] buffer[0:1023];
        reg [8*64-1:0] token;
        real parsed_val;
        integer parsed;
        begin
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
                        if (arg_idx >= 0 && arg_idx < 3 && char_pos > 0) begin
                            parsed = $sscanf(token, "%f", parsed_val);
                            if (parsed == 1)
                                input_v[arg_idx] = parsed_val;
                            else
                                $display("Warning: could not parse positional arg %0d ('%s')", arg_idx + 1, token);
                        end
                        arg_idx = arg_idx + 1;
                        token = {8*64{1'b0}};
                        char_pos = 0;
                    end else if (arg_idx >= 0 && arg_idx < 3 && char_pos < 64) begin
                        token[8*(63-char_pos) +: 8] = buffer[i];
                        char_pos = char_pos + 1;
                    end
                end
            end
        end
    endtask