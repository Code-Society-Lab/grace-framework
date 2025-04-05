from grace.generator import Generator
from re import match
from logging import info
from click.core import Argument
from grace.generators.migration_generator import generate_migration


class ModelGenerator(Generator):
    NAME: str = 'model'
    OPTIONS: dict = {
        "params": [
            Argument(["name"], type=str),
            Argument(["params"], type=str, nargs=-1)
        ],
    }

    def generate(self, name: str, params: tuple[str]):
        """Generate a new model file along its migration.

        The model will be created in the `bot/models` directory with
        a SQLAlchemy-style definition. You can specify column names and types
        during generation using the format `column_name:Type`.

        Supported types are any valid SQLAlchemy column types (e.g., `String`, `Integer`,
        `Boolean`, etc.). See https://docs.sqlalchemy.org/en/20/core/types.html

        Example:
        ```bash
        grace generate model Greeting message:String lang:String
        ```
        """
        info(f"Generating model '{name}'")

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

        generate_migration(self.app, f"Create {name}")

    def validate(self, name: str, **_kwargs) -> bool:
        """Validate the model name.

        A valid model name must:
        - Start with an uppercase letter.
        - Contain only letters (A-Z, a-z) and numbers (0-9).

        Examples of valid names:
        - HelloWorld
        - User123
        - ProductItem
        """
        return bool(match(r'^[A-Z][a-zA-Z0-9]*$', name))

    def extract_columns(self, params: tuple[str]) -> tuple[list, list]:
        columns = []
        types = ['Integer']

        for param in params:
            name, type = param.split(':')

            if type not in types:
                types.append(type)

            columns.append((name, type))

        return columns, types


def generator() -> Generator:
    return ModelGenerator()