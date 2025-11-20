from pathlib import Path


class FunctionLoader:
    def __init__(self, config: dict):
        self.vendor_directory = Path(config["VENDOR_DIRECTORY"])

        self.map = self._get_function_map(self.vendor_directory)

    def _get_function_map(self, directory: Path) -> dict:
        function_map = {"c": {"main": dict(), "regular": dict()}, "verilog": {"main": dict(), "regular": dict()}}
        c_dir = directory / "c"
        verilog_dir = directory / "verilog"

    
        for file in c_dir.glob("main_functions/*.c"):
            function_name = file.stem
            function_map["c"]["main"][function_name] = self._load_file(file)

        for file in c_dir.glob("regular_functions/*.c"):
            function_name = file.stem
            function_map["c"]["regular"][function_name] = self._load_file(file)
    
        for file in verilog_dir.glob("main_functions/*.v"):
            function_name = file.stem
            function_map["verilog"]["main"][function_name] = self._load_file(file)

        for file in verilog_dir.glob("regular_functions/*.v"):
            function_name = file.stem
            function_map["verilog"]["regular"][function_name] = self._load_file(file)
        
        return function_map
    


    def _load_file(self, path: Path) -> str:
        with open(path, "r") as file:
            return file.read()

    def __getitem__(self, function_type: str):
        return self.map[function_type]
