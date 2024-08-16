
import discord
from os import getpid
from logging import info
from click import group, argument, option, pass_context
from grace.generator import register_generators

import os
import sys

APP_INFO = """
| Discord.py version: {discord_version}
| PID: {pid}
| Environment: {env}
| Syncing command: {command_sync}
| Using database: {database} with {dialect}
""".rstrip()


@group()
def cli():
    register_generators(generate)


@cli.group()
def generate():
    pass


@cli.command()
@argument("name")
# This database option is currently disabled since the application and config 
# does not currently support it.
# @option("--database/--no-database", default=True)
@pass_context
def new(ctx, name, database=True):
    cmd = generate.get_command(ctx, 'project')
    ctx.forward(cmd)


@cli.command()
@option("--environment", default='development')
@option("--sync/--no-sync", default=True)
def run(environment=None, sync=None):
    currentdir = os.getcwd()
    sys.path.insert(0, currentdir)

    try:
        from bot import app, run

        _loading_application(app, environment, sync)
        _load_database(app)
        _show_application_info(app)

        run()
    except ImportError:
        print("Unable to find a Grace project in this directory.")


def _loading_application(app, environment, command_sync):
    app.load(environment, command_sync=command_sync)


def _load_database(app):
    if not app.database_exists:
        app.create_database()
        app.create_tables()

def _show_application_info(app):
    print(APP_INFO.format(
        discord_version=discord.__version__,
        env=app.config.current_environment,
        pid=getpid(),
        command_sync=app.command_sync,
        database=app.database_infos["database"],
        dialect=app.database_infos["dialect"],
    ))


def main():
    cli()
