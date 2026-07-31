from logging import fatal, info

from alembic.command import downgrade, revision, upgrade
from alembic.config import Config
from alembic.util.exc import CommandError

from .application import Application
from .exceptions import ConfigError


def generate_migration(app: Application, message: str):
    if not app.has_database:
        raise ConfigError(
            "This project has no database configured. "
            "Run 'grace generate database' to add one."
        )

    try:
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.config_ini_section = app.environment

        revision(alembic_cfg, message=message, autogenerate=True, sql=False)
    except CommandError as e:
        fatal(f"Error creating migration: {e}")


def up_migration(app: Application, revision_: str = "head"):
    info(f"Upgrading revision {revision_}")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.config_ini_section = app.environment

    upgrade(alembic_cfg, revision=revision_)


def down_migration(app: Application, revision_: str = "head"):
    info(f"Downgrading revision {revision_}")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.config_ini_section = app.environment

    downgrade(alembic_cfg, revision=revision_)
