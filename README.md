# Model-Transpiler
This repository contains a tool to transpile machine learning models into different programming languages, such as Verilog and C. The transpiler supports various model types and generates code that can be integrated into hardware or software applications.

## Test examples
### Linear Regression
With the inputs `[1.0, 2.0, 3.0]`, the expected output is `370928.232673`.

### Logistic Regression (Binary)
- **True Positive Case**: Inputs `[0.0, 1.0, 0.0]` with prediction `0.842969`
- **False Positive Case**: Inputs `[0.0, 1.0, 3.0]` with prediction `0.004341`

### Decision Tree
- **Class -1 Prediction**: Inputs `[5.1, 3.5, 0]`
- **Class 0 Prediction**: Inputs `[5.1, 3.5, 1.4]`
- **Class 1 Prediction**: Inputs `[0.0, 0.0, 1.0]`