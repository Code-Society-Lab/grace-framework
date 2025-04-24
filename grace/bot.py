from logging import info, warning, critical
from discord import Intents, LoginFailure
from discord.ext.commands import Bot as DiscordBot, when_mentioned_or
from grace.application import Application, SectionProxy


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

    async def setup_hook(self) -> None:
        await self._load_extensions()

        if self.app.command_sync:
            warning("Syncing application commands. This may take some time.")

            if guild_id := self.config.get("guild"):
                guild = self.get_guild(int(guild_id))
                await self.tree.sync(guild=guild)

    def run(self) -> None: # type: ignore[override]
        """Run the bot

        Override the `run` method to handle the token retrieval
        """
        try:
            if self.app.token:
                super().run(self.app.token)
            else:
                critical("Unable to find the token. Make sure your current"
                         "directory contains an '.env' and that "
                         "'DISCORD_TOKEN' is defined")
        except LoginFailure as e:
            critical(f"Authentication failed : {e}")