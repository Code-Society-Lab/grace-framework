from grace.generator import Generator
from re import match
from logging import info


class DatabaseGenerator(Generator):
    NAME = 'database'
    OPTIONS = {}

    def generate(self, output_dir: str = ""):
        info(f"Creating database at {output_dir}")
        self.generate_template(self.NAME, variables={
            "output_dir": output_dir
        })

    def validate(self, *_args, **_kwargs) -> bool:
        return True


def generator() -> Generator:
    return DatabaseGenerator()