DEPENDENCIES_C = {
    "sigmoid": ["exp_approx"],
    "exp_approx": ["factorial", "pow"],
    "pow": [],
    "factorial": [],
    "logistic_regression": ["sigmoid", "linear_regression", "preprocessing"],
    "linear_regression": ["preprocessing"],
    "decision_tree": ["preprocessing"],
    "relu": [],
    "mlp": ["relu", "preprocessing"],
    "preprocessing": [],
}

# Verilog logistic regression uses a dedicated logistic_linear_regression that reads the
# theta matrix directly; linear_regression remains the 1D variant for pure linear models.
DEPENDENCIES_VERILOG = {
    "sigmoid": ["exp_approx"],
    "exp_approx": ["factorial", "pow"],
    "pow": [],
    "factorial": [],
    "logistic_regression": ["sigmoid", "logistic_linear_regression", "preprocessing"],
    "logistic_linear_regression": [],
    "linear_regression": ["preprocessing"],
    "decision_tree": ["preprocessing"],
    "relu": [],
    "mlp": ["relu", "preprocessing"],
    "preprocessing": [],
}


def get_dependencies(function_name: str, language: str | None = None) -> list:
    """Get all dependencies for a given function, including nested dependencies."""
    if language not in ("c", "verilog"):
        raise ValueError("language must be either 'c' or 'verilog'")
    deps_map = DEPENDENCIES_VERILOG if language == "verilog" else DEPENDENCIES_C

    if function_name not in deps_map:
        return []

    dependencies = list()

    def _get_deps(func_name):
        for dep in deps_map.get(func_name, []):
            if dep not in dependencies:
                _get_deps(dep)
                dependencies.append(dep)

    _get_deps(function_name)
    return list(dependencies)
