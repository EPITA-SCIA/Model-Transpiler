    function real linear_regression;
        input integer dummy;
        integer i;
        real res;
        begin
            res = thetas[0]; // bias term
            for (i = 0; i < 3; i = i + 1)
                res = res + input_v[i] * thetas[i+1];
            linear_regression = res;
        end
    endfunction