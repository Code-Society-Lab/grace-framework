import discord

from sys import path
from os import getpid, getcwd
from logging import info, warning, critical
from click import group, argument, option, pass_context, echo
from grace.generator import register_generators
from grace.database import up_migration, down_migration
from textwrap import dedent


APP_INFO = """
| Discord.py version: {discord_version}
| PID: {pid}
| Environment: {env}
| Syncing command: {command_sync}
| Watcher enabled: {watch}
| Using database: {database} with {dialect}
""".rstrip()


@group()
def cli():
    register_generators(generate)


@cli.command()
@argument("name")
# This database option is currently disabled since the application and config 
# does not currently support it.
# @option("--database/--no-database", default=True)
@pass_context
def new(ctx, name, database=True):
    cmd = generate.get_command(ctx, 'project')
    ctx.forward(cmd)

    echo(dedent(f"""
      Done! Please do :\n
        1. cd {name}
        2. set your token in your .env
        3. grace run
    """))


@group()
@option("--environment", default='development', help="The environment to load.")
@pass_context
def app_cli(ctx, environment):
    app = ctx.obj["app"]

    app.load(environment)
    register_generators(generate)


@app_cli.group()
def generate():
    pass


@app_cli.group()
def db():
    pass


@app_cli.command()
@option("--sync/--no-sync", default=True, help="Sync the application command.")
@option("--watch/--no-watch", default=False, help="Enables hot reload.")
@pass_context
def run(ctx, sync, watch):
    app = ctx.obj["app"]
    bot = ctx.obj["bot"]

    app.watch = watch
    app.command_sync = sync

    _load_database(app)
    _show_application_info(app)

    bot.run()


@db.command()
@pass_context
def create(ctx):
    app = ctx.obj["app"]

    if app.database_exists:
        return warning("Database already exists")

    app.create_database()
    app.create_tables()


@db.command()
@pass_context
def drop(ctx):
    app = ctx.obj["app"]

    if not app.database_exists:
        return warning("Database does not exist")

    app.drop_tables()
    app.drop_database()


@db.command()
@pass_context
def seed(ctx):
    app = ctx.obj["app"]

    if not app.database_exists:
        return warning("Database does not exist")

    from db import seed
    seed.seed_database()


@db.command()
@argument("revision", default='head')
@pass_context
def up(ctx, revision):
    app = ctx.obj["app"]

    if not app.database_exists:
        return warning("Database does not exist")

    up_migration(app, revision)


@db.command()
@argument("revision", default='head')
@pass_context
def down(ctx, revision):
    app = ctx.obj["app"]

    if not app.database_exists:
        return warning("Database does not exist")

    down_migration(app, revision)


def _load_database(app):
    if not app.database_exists:
        app.create_database()
        app.create_tables()


def _show_application_info(app):
    info(APP_INFO.format(
        discord_version=discord.__version__,
        env=app.environment,
        pid=getpid(),
        command_sync=app.command_sync,
        watch=app.watch,
        database=app.database_infos["database"],
        dialect=app.database_infos["dialect"],
    ))


def main():
    path.insert(0, getcwd())

    try:
        from bot import app, bot
        app_cli(obj={"app": app, "bot": bot})
    except ImportError:
        cli()
