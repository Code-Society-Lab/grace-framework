from logging import info, warning

from click.core import Argument

from grace.database import generate_migration
from grace.generator import Generator


class MigrationGenerator(Generator):
    NAME: str = "migration"
    OPTIONS: dict = {
        "params": [
            Argument(["message"], type=str),
        ],
    }

    def generate(self, message: str):
        """Generates a new Alembic migration using autogenerate.

        Example:
        ```bash
        grace generate migration "Add Greeting model"
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

        info(f"Generating migration '{message}'")

        generate_migration(self.app, message)

    def validate(self, message: str, **_kwargs) -> bool:
        """
        Validate the migration message.

        The message must be a non-empty string.

        Example:
        - AddUserModel
        - add_email_to_users
        """
        return bool(message.strip())


def generator() -> Generator:
    return MigrationGenerator()
