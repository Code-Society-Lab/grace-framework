from logging import info
from pathlib import Path
from shutil import copy

from grace.generator import Generator


class DatabaseGenerator(Generator):
    NAME = "database"
    OPTIONS = {}

    def generate(self, output_dir: str = ""):
        info(f"Creating database in '{output_dir or '.'}'")

        self.generate_template(self.NAME, output_dir=output_dir)
        self._copy_config_files(output_dir)

    def _copy_config_files(self, output_dir: str):
        config_dir = Path(output_dir) / "config"
        config_dir.mkdir(parents=True, exist_ok=True)

        source = self.templates_path / self.NAME
        copy(source / "alembic.ini", Path(output_dir) / "alembic.ini")
        copy(source / "database.cfg", config_dir / "database.cfg")

    def validate(self, *_args, **_kwargs) -> bool:
        return True


def generator() -> Generator:
    return DatabaseGenerator()
