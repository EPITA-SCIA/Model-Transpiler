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
