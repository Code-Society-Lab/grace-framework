from bot import app
from logging import info, warning, critical
from discord import Intents, ActivityType, Activity
from discord.ext.commands import Bot, when_mentioned_or


class {{ cookiecutter.__project_class }}(Bot):
    def __init__(self):
        self.config = app.bot

        super().__init__(
            command_prefix=when_mentioned_or(self.config.get("prefix")),
            description=self.config.get("description"),
            intents=Intents.all(),
            activity=Activity(type=ActivityType.playing)
        )

    async def load_extensions(self):
        for module in app.extension_modules:
            info(f"Loading {module}")
            await self.load_extension(module)

    async def on_ready(self):
        info(f"{self.user.name}#{self.user.id} is online and ready to use!")

    async def invoke(self, ctx):
        if ctx.command:
            info(f"'{ctx.command}' has been invoked by {ctx.author} ({ctx.author.display_name})") 
        await super().invoke(ctx)

    async def setup_hook(self):
        await self.load_extensions()

        if app.command_sync:
            warning("Syncing application commands. This may take some time.")

            guild = self.get_guild(app.config.get("client", "guild"))
            await self.tree.sync(guild=guild)
