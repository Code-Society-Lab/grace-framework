# Extensions

Now that we have a model and table for storing tasks, let's give the bot a way to interact with them using **extensions** — modules that group related commands together, discovered and loaded automatically at startup.

An extension is simply a `bot/extensions/*.py` module that defines an async `setup(bot)` function and, conventionally, a [`discord.ext.commands.Cog`](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) subclass. Grace has no custom base class for cogs — it re-exports `discord.ext.commands` directly (`from grace import Cog, hybrid_command, ...`), and discovers any module under `bot/extensions/` that exposes `setup` (see `Application.extension_modules`).

## Generating a Cog

Generate your first cog:

```bash
grace generate cog Task
```

This creates a new module at `bot/extensions/task_cog.py`:

```python
from discord.ext.commands import Cog
from grace.bot import Bot

class TaskCog(Cog, name="Task"):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

async def setup(bot: Bot):
    await bot.add_cog(TaskCog(bot))
```

The cog name must be PascalCase (e.g. `Task`, `TaskManager`). You can optionally pass a description:

```bash
grace generate cog Task "Manage your tasks"
```

This is the starting point for your command logic. `TaskCog` is registered automatically when your bot starts (`Bot.load_extensions`), and you define commands inside it to interact with your models.

## Adding Commands

Start by importing what you need:

```python
from discord.ext.commands import Cog, Context, hybrid_command
from bot.models.task import Task
```

### Listing Tasks

```python
@hybrid_command(name="list")
async def list_tasks(self, ctx: Context):
    tasks = Task.all()

    if not tasks:
        await ctx.send("No tasks found.")
        return

    lines = [f"- {'✅' if t.done else '❌'} [{t.id}] **{t.name}**: {t.description or ''}" for t in tasks]
    await ctx.send("\n".join(lines))
```

This fetches all `Task` records and sends them as a formatted message.

### Adding a Task

```python
@hybrid_command(name="add")
async def add_task(self, ctx: Context, name: str, *, description: str = ""):
    task = Task.create(name=name, description=description, done=False)
    await ctx.send(f"Added task: **{task.name}**")
```

Users can type:
```
/add "Write docs" Finish the getting started guide
```

### Deleting a Task

```python
@hybrid_command(name="delete")
async def delete_task(self, ctx: Context, *, task_id: int):
    task = Task.find(task_id)

    if not task:
        await ctx.send(f"No task found with id '{task_id}'.")
        return

    task.delete()
    await ctx.send(f"Deleted task: **{task.name}** 🗑️")
```

### Marking a Task as Done

```python
@hybrid_command(name="done")
async def done_task(self, ctx: Context, *, task_id: int):
    task = Task.find(task_id)

    if not task:
        await ctx.send(f"No task found with id '{task_id}'.")
        return

    task.update(done=True)
    await ctx.send(f"Marked **{task.name}** as done ✅")
```

### Trying It Out

Since `hybrid_command` registers both a slash command and a text command, you can test with either:

```
/add "Write docs" Finish the migration section
/list
/done 1
::list
::delete 1
```

(`::` is the default prefix set in `config/settings.cfg` — see [Configuration](configuration.md).)

## Next Steps

Once your commands are working, learn how to manage the underlying database from the CLI in [Database Management](database.md), or extend the generator system itself in [Writing Generators](generators.md).
