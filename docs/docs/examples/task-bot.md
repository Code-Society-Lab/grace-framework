# Task Bot

A complete, working task manager bot — the same one built step by step across the [Guides](../guides/index.md). This page shows the finished result end to end.

## 1. Scaffold the Project

```bash
grace new task-bot
cd task-bot
```

Set your token in `.env`:

```
DISCORD_TOKEN=your token here
```

## 2. Generate the Model

```bash
grace generate model Task name:String description:String done:Boolean
grace db up
```

`bot/models/task.py`:

```python
from grace.model import Field, Model


class Task(Model):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    done: bool
```

## 3. Generate the Cog

```bash
grace generate cog Task "Manage your tasks"
```

`bot/extensions/task_cog.py`, filled in with commands:

```python
from discord.ext.commands import Cog, Context, hybrid_command

from bot.models.task import Task
from grace.bot import Bot


class TaskCog(Cog, name="Task", description="Manage your tasks"):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @hybrid_command(name="list")
    async def list_tasks(self, ctx: Context):
        tasks = Task.all()

        if not tasks:
            await ctx.send("No tasks found.")
            return

        lines = [
            f"- {'✅' if t.done else '❌'} [{t.id}] **{t.name}**: {t.description or ''}"
            for t in tasks
        ]
        await ctx.send("\n".join(lines))

    @hybrid_command(name="add")
    async def add_task(self, ctx: Context, name: str, *, description: str = ""):
        task = Task.create(name=name, description=description, done=False)
        await ctx.send(f"Added task: **{task.name}**")

    @hybrid_command(name="delete")
    async def delete_task(self, ctx: Context, *, task_id: int):
        task = Task.find(task_id)

        if not task:
            await ctx.send(f"No task found with id '{task_id}'.")
            return

        task.delete()
        await ctx.send(f"Deleted task: **{task.name}** 🗑️")

    @hybrid_command(name="done")
    async def done_task(self, ctx: Context, *, task_id: int):
        task = Task.find(task_id)

        if not task:
            await ctx.send(f"No task found with id '{task_id}'.")
            return

        task.update(done=True)
        await ctx.send(f"Marked **{task.name}** as done ✅")


async def setup(bot: Bot):
    await bot.add_cog(TaskCog(bot))
```

## 4. Run It

```bash
grace run --watch
```

```
/add "Write docs" Finish the getting started guide
/list
/done 1
/delete 1
```

See [Models & Migrations](../guides/models.md) and [Extensions](../guides/extensions.md) for the full explanation of each piece.
