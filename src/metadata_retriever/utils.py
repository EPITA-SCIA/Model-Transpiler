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
    else:
        raise ValueError(f"Unsupported language: {language}")

def _get_matrix(python_matrix: list, language: str) -> str:
    rows = [_get_list(row, language) for row in python_matrix]
    if language == "c":
        return "{" + ", ".join(rows) + "}"
    else:
        raise ValueError(f"Unsupported language: {language}")
    
def get_int_list_definition(name: str, python_list: list, language: str):
    if language == "c":
        return f"int {name}[{len(python_list)}] = " + _get_list(python_list, language) + ";"
    else:
        raise ValueError(f"Unsupported language: {language}")
    
def get_double_list_definition(name: str, python_list: list, language: str):
    if language == "c":
        return f"double {name}[{len(python_list)}] = " + _get_list(python_list, language) + ";"
    else:
        raise ValueError(f"Unsupported language: {language}")

def get_string_list_definition(name: str, python_list: list, language: str):
    if language == "c":
        return f"char *{name}[{len(python_list)}] = " + _get_list(map(lambda x : f"\"{str(x)}\"", python_list), language) + ";"
    else:
        raise ValueError(f"Unsupported language: {language}")
    
def get_double_matrix_definition(name: str, python_matrix: list, language: str):
    if language == "c":
        return f"double {name}[{len(python_matrix)}][{len(python_matrix[0])}] = " + _get_matrix(python_matrix, language) + ";"
    else:
        raise ValueError(f"Unsupported language: {language}")
    
def get_int_definition(name: str, value: int, language: str) -> str:
    if language == "c":
        return f"int {name} = {value};"
    else:
        raise ValueError(f"Unsupported language: {language}")
    
def get_double_definition(name: str, value: float, language: str) -> str:
    if language == "c":
        return f"double {name} = {value};"
    else:
        raise ValueError(f"Unsupported language: {language}")
    
def get_bool_definition(name: str, value: bool, language: str) -> str:
    if language == "c":
        return f"bool {name} = {str(value).lower()};"
    else:
        raise ValueError(f"Unsupported language: {language}")