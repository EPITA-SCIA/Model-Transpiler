function real sigmoid;
    input real x;
    begin
        sigmoid = 1.0 / (1.0 + exp_approx(-x, 10));
    end
endfunction