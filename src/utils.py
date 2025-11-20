from pathlib import Path
import joblib

def load_models(paths) -> list:
    models = []
    for path in paths:
        model = joblib.load(path)
        models.append(model)
    return models

def write_to_file(path: Path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w+") as f:
        f.write(content)
    return path