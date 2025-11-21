def get_preprocessing_id(preprocessing: str) -> int:
    if preprocessing is None:
        return 0  # No preprocessing
    elif preprocessing == "min_max_scaler":
        return 1
    else:
        raise ValueError(f"Unknown preprocessing type: {preprocessing}")


def _get_list(python_list: list, language: str, _verilog_list_name: str = None) -> str:
    if language == "c":
        assert _verilog_list_name is None
        return "{" + ", ".join(str(x) for x in python_list) + "}"
    elif language == "verilog":
        assert _verilog_list_name is not None
        return (
            "initial begin\n"
            + "\n".join(
                f"{_verilog_list_name}[{i}] = {str(el)};"
                for i, el in enumerate(python_list)
            )
            + "\nend"
        )
    else:
        raise ValueError(f"Unsupported language: {language}")


def _get_matrix(
    python_matrix: list, language: str, _verilog_list_name: str = None
) -> str:
    if language == "c":
        assert _verilog_list_name is None
        rows = [_get_list(row, language, _verilog_list_name) for row in python_matrix]
        return "{" + ", ".join(rows) + "}"
    elif language == "verilog":
        assert _verilog_list_name is not None
        return (
            "initial begin\n"
            + "\n".join(
                f"{_verilog_list_name}[{i}][{j}] = {str(python_matrix[i][j])};"
                for i in range(len(python_matrix))
                for j in range(len(python_matrix[i]))
            )
            + "\nend"
        )

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
        return f"reg integer {name}[0:{len(python_list) - 1}];\n" + _get_list(
            python_list, language, _verilog_list_name=name
        )
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
        return f"reg real {name}[0:{len(python_list) - 1}];\n" + _get_list(
            python_list, language, _verilog_list_name=name
        )
    else:
        raise ValueError(f"Unsupported language: {language}")


def get_string_list_definition(name: str, python_list: list, language: str):
    # Materialize as strings to handle non-string labels (e.g., bools)
    stringified = [str(x) for x in python_list]
    if language == "c":
        return (
            f"char *{name}[{len(stringified)}] = "
            + _get_list(map(lambda x: f'"{x}"', stringified), language)
            + ";"
        )
    elif language == "verilog":
        max_length = len(max(map(lambda x: f'"{x}"', stringified), key=len))
        return (
            f"reg [8*{max_length}-1:0] {name}[0:{len(stringified) - 1}];\n"
            + _get_list(
                map(lambda x: f'"{x}"', stringified),
                language,
                _verilog_list_name=name,
            )
        )
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
        return (
            f"reg real {name}[0:{len(python_matrix) - 1}][0:{len(python_matrix[0]) - 1}];\n"
            + _get_matrix(python_matrix, language, _verilog_list_name=name)
        )
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
        return f"integer {name} = {int(value)};"
    else:
        raise ValueError(f"Unsupported language: {language}")
