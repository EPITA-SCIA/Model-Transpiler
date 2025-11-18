DEPENDENCIES = {
    "sigmoid": ["exp_approx"],
    "exp_approx": ["factorial", "pow"],
    "pow": [],
    "factorial": [],
    "logistic_regression": ["sigmoid", "linear_regression"],
    "linear_regression": [],
    "decision_tree": [],
}


def get_dependencies(function_name: str) -> list:
    """Get all dependencies for a given function, including nested dependencies."""
    if function_name not in DEPENDENCIES:
        return []

    dependencies = list()

    def _get_deps(func_name):
        for dep in DEPENDENCIES.get(func_name, []):
            if dep not in dependencies:
                _get_deps(dep)
                dependencies.append(dep)

    _get_deps(function_name)
    return list(dependencies)
