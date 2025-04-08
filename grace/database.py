from alembic.config import Config
from alembic.command import revision, upgrade, downgrade, show
from alembic.util.exc import CommandError
from logging import info, fatal

from alembic.script import ScriptDirectory


def generate_migration(app, message):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.config_ini_section = app.config.current_environment

    try:
        revision(
            alembic_cfg,
            message=message,
            autogenerate=True,
            sql=False
        )
    except CommandError as e:
        fatal(f"Error creating migration: {e}")


def up_migration(app, revision='head'):
    info(f"Upgrading revision {revision}")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.config_ini_section = app.config.current_environment

    upgrade(alembic_cfg, revision=revision)


def down_migration(app, revision='head'):
    info(f"Downgrading revision {revision}")

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.config_ini_section = app.config.current_environment

    downgrade(alembic_cfg, revision=revision)
