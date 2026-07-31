# Scheduled Tasks

Every `Bot` instance carries an [APScheduler](https://apscheduler.readthedocs.io/) `AsyncIOScheduler` as `bot.scheduler`, started automatically in `setup_hook` when the bot connects. Any cog can schedule jobs against it.

This example extends the [task bot](task-bot.md) with a daily reminder of open tasks.

`bot/extensions/task_cog.py`:

```python
from discord.ext.commands import Cog

from bot.models.task import Task
from grace.bot import Bot


class TaskCog(Cog, name="Task"):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

        self.bot.scheduler.add_job(
            self.remind_open_tasks,
            "cron",
            hour=9,
            id="task_reminder",
        )

    async def remind_open_tasks(self):
        open_tasks = Task.where(done=False).all()

        if not open_tasks:
            return

        channel = self.bot.get_channel(REMINDER_CHANNEL_ID)
        lines = [f"- [{t.id}] **{t.name}**" for t in open_tasks]

        await channel.send("Open tasks:\n" + "\n".join(lines))


async def setup(bot: Bot):
    await bot.add_cog(TaskCog(bot))
```

`add_job` accepts any [APScheduler trigger](https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html) — `"cron"`, `"interval"`, or `"date"` — with the same keyword arguments you'd use with APScheduler directly, since `bot.scheduler` is an unmodified `AsyncIOScheduler`.

!!! tip
    Give jobs an explicit `id` so re-adding them (e.g. after a `--watch` reload) replaces rather than duplicates the job — see [Hot Reload](hot-reload.md).
