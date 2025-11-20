    function real factorial;
        input integer a;
        real res;
        begin
            res = 1.0;
            while (a > 0) begin
                res = res * a;
                a = a - 1;
            end
            factorial = res;
        end
    endfunction