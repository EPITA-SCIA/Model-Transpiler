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
