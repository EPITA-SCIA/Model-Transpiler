function real logistic_regression;
    input integer dummy;
    begin
        logistic_regression = sigmoid(linear_regression(0));
    end
endfunction