from grace.generator import Generator
from re import match
from logging import info
from click.core import Argument


class CogGenerator(Generator):
    NAME: str = 'cog'
    OPTIONS: dict = {
        "params": [
            Argument(["name"], type=str),
            Argument(["description"], type=str, required=False, default="")
        ],
    }

    def generate(self, name: str, description: str = ""):
        info(f"Creating cog '{name}'")

        self.generate_file(
            self.NAME,
            variables={
                "cog_name": name,
                "cog_description": description,
            },
            output_dir="bot/extensions"
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


def generator() -> Generator:
    return CogGenerator()