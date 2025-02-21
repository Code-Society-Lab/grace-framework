from grace.generator import Generator
from re import match
from logging import info


class DatabaseGenerator(Generator):
    NAME = 'database'
    OPTIONS = {}

    def generate(self, output_dir: str = ""):
        info(f"Creating database")
        self.generate_template(self.NAME, output_dir=output_dir)

    def validate(self, *_args, **_kwargs) -> bool:
        return True


def generator() -> Generator:
    return DatabaseGenerator()