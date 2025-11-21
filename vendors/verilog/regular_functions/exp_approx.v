    function real exp_approx;
        input real x;
        input integer n_term;
        integer i;
        real res;
        begin
            if (x < 0)
                exp_approx = 1.0 / exp_approx(-x, n_term);
            else begin
                res = 0.0;
                for (i = 0; i <= n_term; i = i + 1)
                    res = res + pow(x, i) / factorial(i);
                exp_approx = res;
            end
        end
    endfunction
