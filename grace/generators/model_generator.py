from logging import info, warning
from re import match

from click.core import Argument
from jinja2_strcase.jinja2_strcase import to_snake

from grace.exceptions import ValidationError
from grace.generator import Generator
from grace.generators.migration_generator import generate_migration

# Field annotations must be plain Python types Pydantic can build a schema for,
# not SQLAlchemy column type classes (e.g. `str`, not `String`) - see
# https://docs.pydantic.dev/latest/concepts/types/ for what's supported.
COLUMN_TYPES: dict[str, str] = {
    "String": "str",
    "Text": "str",
    "Integer": "int",
    "Float": "float",
    "Boolean": "bool",
}


class ModelGenerator(Generator):
    NAME: str = "model"
    OPTIONS: dict = {
        "params": [
            Argument(["name"], type=str),
            Argument(["params"], type=str, nargs=-1),
        ],
    }

    def generate(self, name: str, params: tuple[str]):
        """Generate a new model file along its migration.

        The model will be created in the `bot/models` directory with
        a SQLAlchemy-style definition. You can specify column names and types
        during generation using the format `column_name:Type`.

        Supported types: String, Text, Integer, Float, Boolean.

        Example:
        ```bash
        grace generate model Greeting message:String lang:String
        ```
        """
        if not self.app:
            raise ValueError("app is not initialized")

        if not self.app.has_database:
            warning(
                "This project has no database configured. "
                "Run 'grace generate database' to add one."
            )
            return

        info(f"Generating model '{name}'")

        columns, types = self.extract_columns(params)
        model_columns = map(lambda c: f"{c[0]}: {c[1]}", columns)

        self.generate_file(
            self.NAME,
            variables={
                "model_name": name,
                "model_module_name": to_snake(name),
                "model_columns": model_columns,
                "model_column_types": types,
            },
            output_dir="bot/models",
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
        return bool(match(r"^[A-Z][a-zA-Z0-9]*$", name))

    def extract_columns(self, params: tuple[str]) -> tuple[list, list]:
        columns = []
        types = []

        for param in params:
            name, type_ = param.split(":")

            if type_ not in COLUMN_TYPES:
                raise ValidationError(
                    f"Unsupported column type '{type_}' for '{name}'. "
                    f"Supported types: {', '.join(sorted(COLUMN_TYPES))}."
                )

            python_type = COLUMN_TYPES[type_]

            if python_type not in types:
                types.append(python_type)

            columns.append((name, python_type))

        return columns, types


def generator() -> Generator:
    return ModelGenerator()
