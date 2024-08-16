from logging import info, warning, critical
from discord import LoginFailure, Intents, ActivityType, Activity
from discord.ext.commands import Bot as DiscordBot, when_mentioned_or


class Bot(DiscordBot):
    def __init__(self, app, **kwargs):
        self.app = app
        self.config = self.app.client

        intents = kwargs.get("intents", Intents.default())

        super().__init__(
            command_prefix=when_mentioned_or(self.config.get("prefix")),
            description=self.config.get("description"),
            activity=Activity(type=ActivityType.playing),
            intents=intents,
        )

    async def _load_extensions(self):
        for module in self.app.extension_modules:
            info(f"Loading module '{module}'")
            await self.load_extension(module)

    async def setup_hook(self):
        await self._load_extensions()

        if self.app.command_sync:
            warning("Syncing application commands. This may take some time.")

            guild = self.get_guild(self.config.get("client", "guild"))
            await self.tree.sync(guild=guild)

    def run(self):
        try:
            if self.app.token:
                super().run(self.app.token)
            else:
                critical("Unable to find the token. Make sure your current"
                         "directory contains an '.env' and that "
                         "'DISCORD_TOKEN' is defined")
        except LoginFailure as e:
            critical(f"Authentication failed : {e}")