# Bot

The `Bot` class is a subclass of [`discord.ext.commands.Bot`](https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#bot) and drives your bot's lifecycle: loading extensions, syncing application commands, running the scheduler, and — when enabled — hot-reloading on file changes.

```python
from logging import info

from grace.bot import Bot


class TaskBot(Bot):
    async def on_ready(self):
        info(f"{self.user.name}:#{self.user.id} is online and ready to use!")
```

::: grace.bot.Bot
