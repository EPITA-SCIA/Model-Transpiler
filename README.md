# Model-Transpiler

Model-Transpiler converts trained machine-learning models into standalone C or Verilog
programs. It lets you take classic scikit-learn estimators or lightweight PyTorch MLPs
and run them on hardware targets or bare-metal environments without a Python runtime.

The CLI introspects a serialized model, gathers the metadata it needs (weights,
pre-processing parameters, topology, etc.), and stitches that information into
language-specific templates located in `vendors/`. The generated sources can be built
with `gcc` or `iverilog` and are validated by an integration test-suite under `tests/`.

## Supported inputs

| Format | Details |
| ------ | ------- |
| `.joblib` | Any scikit-learn `LinearRegression`, `LogisticRegression` (binary or multi-class), `DecisionTreeClassifier`, or a `Pipeline` that optionally includes a `MinMaxScaler` before one of those estimators. |
| `.pt` / `.pth` | PyTorch state_dict files describing an `nn.Sequential` multilayer perceptron composed of `Linear` layers with optional `ReLU` activations. |

> The metadata retrievers live in `src/metadata_retriever/`. Add a new retriever and
> update `src/utils.get_metadata_retriever_class` to support additional model types.

## Repository layout

- `main.py` – CLI that loads a serialized model, chooses the target language(s), and writes sources to `outputs/`.
- `src/` – Core transpiler logic, including metadata extraction, dependency resolution, and template loading.
- `vendors/` – Vendor-provided snippets split into `c/` and `verilog/` directories with `regular_functions/` and `main_functions/`.
- `models/` – Sample models you can transpile immediately.
- `tests/test_pipeline.py` – End-to-end tests that transpile, compile, and execute every sample model.
- `benchmark.sh` / `time_inference.py` – Utilities to compare Python inference time against generated binaries.

## Transpiling models

```bash
python main.py --path models/linear.joblib --c --v
```

- `--path` points to any supported `.joblib`, `.pt`, or `.pth` file.
- Pass `--c` and/or `--v` to restrict languages; omit both to emit **both**.
- Outputs land in `outputs/<model_name>.c` or `.v`. Existing files are overwritten.

You can now compile and run the generated programs:

```bash
gcc outputs/linear.c -o outputs/linear_c.out
outputs/linear_c.out 1 2 3

iverilog -o outputs/linear_v.out outputs/linear.v
vvp outputs/linear_v.out 1 2 3
```

### Using your own templates

`main.py` loads `.config` to find the vendor directory:

```ini
[FunctionLoader]
VENDOR_DIRECTORY = ./vendors
```

Point it to another folder to swap in different runtime implementations. Each regular
function can declare dependencies in `src/dependencies.py`; the transpiler resolves and
inlines those snippets automatically for the chosen language.

## Testing

The integration tests ensure end-to-end parity between Python predictions and the
generated binaries (including preprocessing paths).

```bash
pytest tests/test_pipeline.py
```

Tests expect `gcc` and `iverilog` on `PATH`. They create temporary directories, so no
artifacts remain in `outputs/`.

## Benchmarking

`benchmark.sh` transpiles every model in `models/`, builds the outputs, and compares the
runtime of:

1. Native Python via `time_inference.py`
2. Compiled C binary
3. Compiled Verilog simulation

The script requires `hyperfine`, `gcc`, and `iverilog`. Results are written to stdout
alongside the generated `outputs/<name>_{c,v}.out` binaries.

