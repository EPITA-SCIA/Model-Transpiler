    function real logistic_regression;
        input integer dummy;
        begin
            logistic_regression = sigmoid(linear_regression(0));
        end
    endfunction

    // Compatibility wrappers: some mains call `*_prediction` names
    function real linear_prediction;
        input integer dummy;
        begin
            linear_prediction = linear_regression(dummy);
        end
    endfunction

    function real logistic_prediction;
        input integer dummy;
        begin
            logistic_prediction = logistic_regression(dummy);
        end
    endfunction