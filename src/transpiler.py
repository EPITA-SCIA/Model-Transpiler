from pathlib import Path

from src.dependencies import get_dependencies
from src.function_loader import FunctionLoader
from src.utils import get_metadata_retriever_class, write_to_file


class Transpiler:
    __slots__ = ("model", "language", "output_file")

    def __init__(self, model, language: str, output_file: Path):
        self.model = model
        self.language = language
        self.output_file = output_file

    def transpile(self, function_loader: FunctionLoader):
        if self.language == "c":
            self._transpile_to_c(function_loader)
        elif self.language == "verilog":
            self._transpile_to_verilog(function_loader)
        else:
            raise ValueError(f"Unsupported language: {self.language}")

    def _transpile_to_c(self, function_loader: FunctionLoader):
        res = ""

        metadata_retriever = get_metadata_retriever_class(model=self.model)(
            model=self.model, language=self.language
        )

        metadata, model_name = metadata_retriever.retrieve_metadata()

        res += function_loader[self.language]["regular"]["includes"] + "\n"
        res += "\n".join(metadata) + "\n"

        dependencies = get_dependencies(model_name, self.language)
        for dep in dependencies:
            res += function_loader[self.language]["regular"][dep]

        res += function_loader[self.language]["regular"][model_name]
        res += function_loader[self.language]["main"][model_name]
        write_to_file(self.output_file, res)

    def _transpile_to_verilog(self, function_loader: FunctionLoader):
        res = "module main;\n"

        metadata_retriever = get_metadata_retriever_class(model=self.model)(
            model=self.model, language=self.language
        )

        metadata, model_name = metadata_retriever.retrieve_metadata()
        res += "\n".join(metadata) + "\n"

        dependencies = get_dependencies(model_name, self.language)
        for dep in dependencies:
            res += function_loader[self.language]["regular"][dep]

        res += function_loader[self.language]["regular"][model_name]

        res += function_loader[self.language]["main"]["argparse"]
        res += function_loader[self.language]["main"][model_name]

        res += "endmodule\n"

        write_to_file(self.output_file, res)
