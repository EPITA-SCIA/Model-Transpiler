def get_preprocessing_id(preprocessing: str) -> int:
    if preprocessing is None:
        return 0  # No preprocessing
    elif preprocessing == "min_max_scaler":
        return 1
    else:
        raise ValueError(f"Unknown preprocessing type: {preprocessing}")


def _get_list(python_list: list, language: str) -> str:
    if language == "c":
        return "{" + ", ".join(str(x) for x in python_list) + "}"
    elif language == "verilog":

        def _fmt(x):
            # format values for Verilog: strings quoted, booleans as 1/0, floats with decimal
            if isinstance(x, str):
                return f'"{x}"'
            if isinstance(x, bool):
                return "1'b1" if x else "1'b0"
            # For numpy types fallback to python scalars
            try:
                # int-like
                if float(x).is_integer():
                    return str(int(x))
            except Exception:
                pass
            # default: preserve decimal point for reals
            return str(float(x))

        return ", ".join(_fmt(x) for x in python_list)
    else:
        raise ValueError(f"Unsupported language: {language}")


def _get_matrix(python_matrix: list, language: str) -> str:
    rows = [_get_list(row, language) for row in python_matrix]
    if language == "c":
        return "{" + ", ".join(rows) + "}"
    elif language == "verilog":
        # return flattened comma-separated with explicit indices handled by caller
        # produce nested list strings suitable for iterating
        return "; ".join(", ".join(str(x) for x in r) for r in rows)
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_int_list_definition(name: str, python_list: list, language: str):
    if language == "c":
        return (
            f"int {name}[{len(python_list)}] = "
            + _get_list(python_list, language)
            + ";"
        )
    elif language == "verilog":
        if len(python_list) == 0:
            return f"// empty integer array {name}"
        decl = f"integer {name}[0:{len(python_list) - 1}];"
        init_lines = "\n".join(
            f"    {name}[{i}] = {int(v)};" for i, v in enumerate(python_list)
        )
        return decl + "\ninitial begin\n" + init_lines + "\nend"
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_double_list_definition(name: str, python_list: list, language: str):
    if language == "c":
        return (
            f"double {name}[{len(python_list)}] = "
            + _get_list(python_list, language)
            + ";"
        )
    elif language == "verilog":
        if len(python_list) == 0:
            return f"// empty real array {name}"
        decl = f"real {name}[0:{len(python_list) - 1}];"

        def _fmt(v):
            try:
                if float(v).is_integer():
                    return f"{int(v)}.0"
            except Exception:
                pass
            return str(float(v))

        init_lines = "\n".join(
            f"    {name}[{i}] = {_fmt(v)};" for i, v in enumerate(python_list)
        )
        return decl + "\ninitial begin\n" + init_lines + "\nend"
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_string_list_definition(name: str, python_list: list, language: str):
    if language == "c":
        return (
            f"char *{name}[{len(python_list)}] = "
            + _get_list(map(lambda x: f'"{str(x)}"', python_list), language)
            + ";"
        )
    elif language == "verilog":
        # Emit plain Verilog-compatible reg vectors for strings so simulators
        # that don't support SystemVerilog `string` (e.g. Icarus/iverilog)
        if len(python_list) == 0:
            return f"// empty string array {name}"
        # determine max length (in bytes) of strings
        strs = [str(v) for v in python_list]
        max_len = max(len(s) for s in strs)
        decl = f"reg [8*{max_len}-1:0] {name}[0:{len(strs) - 1}];"
        init_lines = "\n".join(f'    {name}[{i}] = "{s}";' for i, s in enumerate(strs))
        return decl + "\ninitial begin\n" + init_lines + "\nend"
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_double_matrix_definition(name: str, python_matrix: list, language: str):
    if language == "c":
        return (
            f"double {name}[{len(python_matrix)}][{len(python_matrix[0])}] = "
            + _get_matrix(python_matrix, language)
            + ";"
        )
    elif language == "verilog":
        if len(python_matrix) == 0 or len(python_matrix[0]) == 0:
            return f"// empty matrix {name}"
        nrows = len(python_matrix)
        ncols = len(python_matrix[0])
        # Flatten to 1-D array to avoid iverilog multi-dim assignment issues
        # Access via: {name}_flat[row*ncols + col]
        flat_size = nrows * ncols
        decl = f"real {name}_flat[0:{flat_size - 1}];"
        init_lines = []
        for i, row in enumerate(python_matrix):
            for j, val in enumerate(row):
                flat_idx = i * ncols + j
                init_lines.append(f"    {name}_flat[{flat_idx}] = {float(val)};")
        # Add helper function to access matrix
        helper = f"""
    // Helper function to index {name} as 2D via flattened array
    function real {name};
        input integer row;
        input integer col;
        begin
            {name} = {name}_flat[row * {ncols} + col];
        end
    endfunction"""
        return decl + "\ninitial begin\n" + "\n".join(init_lines) + "\nend" + helper
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_int_definition(name: str, value: int, language: str) -> str:
    if language == "c":
        return f"int {name} = {value};"
    elif language == "verilog":
        return f"integer {name} = {int(value)};"
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_double_definition(name: str, value: float, language: str) -> str:
    if language == "c":
        return f"double {name} = {value};"
    elif language == "verilog":
        return f"real {name} = {float(value)};"
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_bool_definition(name: str, value: bool, language: str) -> str:
    if language == "c":
        return f"bool {name} = {str(value).lower()};"
    elif language == "verilog":
        return f"integer {name} = {1 if value else 0};"
    else:
        raise ValueError(f"Unsupported language: {language}")
