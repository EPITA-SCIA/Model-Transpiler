    function real relu;
        input real x;
        begin
            if (x > 0.0)
                relu = x;
            else
                relu = 0.0;
        end
    endfunction
