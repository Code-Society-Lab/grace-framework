from logging import info, warning, critical
from discord import Intents, LoginFailure
from discord.ext.commands import Bot as DiscordBot, when_mentioned_or
from discord.ext.commands.errors import (
    ExtensionNotLoaded,
    ExtensionAlreadyLoaded
)
from grace.application import Application, SectionProxy
from grace.watcher import Watcher, Observer


class Bot(DiscordBot):
    """This class is the core of the bot

    This class is a subclass of `discord.ext.commands.Bot` and is the core
    of the bot. It is responsible for loading the extensions and 
    syncing the commands.

    The bot is instantiated with the application object and the intents.
    """

    def __init__(self, app: Application, **kwargs):
        self.app: Application = app
        self.config: SectionProxy = self.app.client
        self.watcher: Watcher = Watcher(self.on_reload)

        command_prefix = kwargs.pop(
            'command_prefix',
            when_mentioned_or(self.config.get("prefix", "!"))
        )
        description: str = kwargs.pop(
            'description',
            self.config.get("description")
        )
        intents: Intents = kwargs.pop(
            'intents',
            Intents.default()
        )

        super().__init__(
            command_prefix=command_prefix,
            description=description,
            intents=intents,
            **kwargs
        )

    async def _load_extensions(self) -> None:
        for module in self.app.extension_modules:
            info(f"Loading module '{module}'")
            await self.load_extension(module)

    async def _sync_commands(self) -> None:
        warning("Syncing application commands. This may take some time.")

        if guild_id := self.config.get("guild"):
            guild = self.get_guild(int(guild_id))
            await self.tree.sync(guild=guild)

    async def invoke(self, ctx):
        if ctx.command:
            info(f"'{ctx.command}' has been invoked by {ctx.author} "
                 f"({ctx.author.display_name})")
        await super().invoke(ctx)

    async def setup_hook(self) -> None:
        await self._load_extensions()

        if self.app.command_sync:
            await self._sync_commands()

        if self.app.watch:
            self.watcher.start()

    async def load_extension(self, name: str) -> None:
        try:
            await super().load_extension(name)
        except ExtensionAlreadyLoaded:
            warning(f"Extension '{name}' already loaded, skipping.")

    async def unload_extension(self, name: str) -> None:
        try:
            await super().unload_extension(name)
        except ExtensionNotLoaded:
            warning(f"Extension '{name}' was not loaded, skipping.")

    async def on_reload(self):
        for module in self.app.extension_modules:
            info(f"Reloading extension '{module}'")

            await self.unload_extension(module)
            await self.load_extension(module)

    def run(self) -> None: # type: ignore[override]
        """Override the `run` method to handle the token retrieval"""
        try:
            if self.app.token:
                super().run(self.app.token)
            else:
                critical("Unable to find the token. Make sure your current"
                         "directory contains an '.env' and that "
                         "'DISCORD_TOKEN' is defined")
        except LoginFailure as e:
            critical(f"Authentication failed : {e}")