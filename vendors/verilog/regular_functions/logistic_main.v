// Fixed-size arrays (n features)
real input[0:{n-1}];
real thetas[0:{n}]; // n features + bias
real pred;
integer max_i;
initial begin
    // Initialize inputs
    {input_init}

    // Initialize weights
    {thetas_init}

    // Prediction
    pred = logistic_prediction(0);
    max_i = (pred < 0.5) ? 0 : 1;

    $display("Prediction: %f", pred);
    $display("Predicted class: %s", (max_i == 0 ? "False" : "True"));
    $finish;
end