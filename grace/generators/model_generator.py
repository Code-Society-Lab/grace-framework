from grace.generator import Generator
from re import match
from logging import info
from click.core import Argument


class ModelGenerator(Generator):
    NAME: str = 'model'
    OPTIONS: dict = {
        "params": [
            Argument(["name"], type=str),
            Argument(["params"], type=str, nargs=-1)
        ],
    }

    def generate(self, name: str, params: tuple[str]):
        info(f"Creating model '{name}'")

        columns, types = self.extract_columns(params)
        model_columns = map(lambda c: f"{c[0]} = Column({c[1]})", columns)

        self.generate_file(
            self.NAME,
            variables={
                "model_name": name,
                "model_columns": model_columns,
                "model_column_types": types
            },
            output_dir="bot/models"
        )

    def validate(self, name: str, **_kwargs) -> bool:
        """Validate the cog name.

        A valid project name must be 'PascalCase' and contain only
        - letters [Aa - Zz]
        - numbers [0-9]

        Example:
        - HelloWorld
        """
        return bool(match(r'^[A-Z][a-zA-Z0-9]*$', name))

    def extract_columns(self, params: tuple[str]) -> tuple[list, list]:
        columns = []
        types = []

        for param in params:
            name, type = param.split(':')

            if type not in types and type != 'Integer':
                types.append(type)

            columns.append((name, type))

        return columns, types


def generator() -> Generator:
    return ModelGenerator()