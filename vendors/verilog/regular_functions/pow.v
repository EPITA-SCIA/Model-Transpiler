    // Integer power approximation matching the C helper `pow`
    function real pow;
        input real a;
        input integer b;
        integer i;
        real res;
        begin
            res = 1.0;
            for (i = 0; i < b; i = i + 1)
                res = res * a;
            pow = res;
        end
    endfunction
