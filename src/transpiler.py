from pathlib import Path

from src.dependencies import get_dependencies
from src.function_loader import FunctionLoader
from src.metadata_retriever.metadata_retriever import MetadataRetriever
from src.utils import write_to_file


class Transpiler:
    __slots__ = ("model", "language", "output_file")

    def __init__(self, model, language: str, output_file: Path):
        self.model = model
        self.language = language
        self.output_file = output_file

    def transpile(self, function_loader: FunctionLoader):
        res = ""
        if self.language == "verilog":
            res += "module compiled_model;\n"

        metadata_retriever = MetadataRetriever(model=self.model, language=self.language)
        metadata, model_name = metadata_retriever.retrieve_metadata()
        res += function_loader[self.language]["regular"]["includes"] + "\n"
        res += "\n".join(metadata) + "\n"
        dependencies = get_dependencies(model_name)
        for dep in dependencies:
            res += function_loader[self.language]["regular"][dep]
        res += function_loader[self.language]["regular"][model_name]

        if self.language == "verilog":
            # Every model will have a part to parse inputs
            res += function_loader[self.language]["main"]["argparse"]
        res += function_loader[self.language]["main"][model_name]
        if self.language == "verilog":
            res += "endmodule\n"
        write_to_file(self.output_file, res)
