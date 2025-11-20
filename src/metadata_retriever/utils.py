def get_preprocessing_id(preprocessing: str) -> int:
    if preprocessing is None:
        return 0  # No preprocessing
    elif preprocessing == "min_max_scaler":
        return 1
    else:
        raise ValueError(f"Unknown preprocessing type: {preprocessing}")

def get_list(python_list: list, language: str) -> str:
    if language == "c":
        return "{" + ", ".join(str(x) for x in python_list) + "}"
    else:
        raise ValueError(f"Unsupported language: {language}")

def get_matrix(python_matrix: list, language: str) -> str:
    rows = [get_list(row, language) for row in python_matrix]
    if language == "c":
        return "{" + ", ".join(rows) + "}"
    else:
        raise ValueError(f"Unsupported language: {language}")

def get_string_list(python_list: list, language: str):
    if language == "c":
        return get_list(map(lambda x : f"\"{str(x)}\"", python_list), language)
    else:
        raise ValueError(f"Unsupported language: {language}")