from click import group, argument, option, pass_context
from grace.generator import register_generators


@group()
def cli():
    pass


@cli.group()
def generate():
    pass


@cli.command()
@argument("name")
@option("--database/--no-database", default=True)
@pass_context
def new(ctx, name, database=True):
    cmd = generate.get_command(ctx, 'project')
    ctx.forward(cmd)


@cli.command()
def start():
    import bot
    bot.start()


def run():
    register_generators(generate)

    cli()
