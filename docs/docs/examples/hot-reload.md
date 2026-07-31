# Hot Reload

During development, restarting your bot after every code change is slow. The `--watch` flag on `grace run` keeps the process alive and reloads your extensions in place whenever a file under `./bot` changes.

```bash
grace run --watch
```

## How It Works

`--watch` sets `app.watch = True`. On `setup_hook`, `Bot` starts a [`Watcher`](../reference/watcher.md) that observes the `./bot` directory recursively using [watchdog](https://python-watchdog.readthedocs.io/). When a `.py` file is created, modified, or deleted, the corresponding module is reloaded, and `Bot.on_reload` unloads then reloads every extension so the new code takes effect.

```python
# bot/extensions/task_cog.py — edit and save while the bot is running

@hybrid_command(name="ping")
async def ping(self, ctx):
    await ctx.send("pong")  # this shows up next command sync, no restart needed
```

## What Gets Reloaded

The watcher reloads extension modules — everything discovered via `app.extension_modules` (i.e. `bot/extensions/*.py` files exposing `setup`). Changes to models, config files, or code outside `bot/` still require a restart.

## Disabling It

`--watch` is off by default (`grace run` alone does not enable it) — it's meant for local development, not production:

```bash
grace run --no-watch   # equivalent to plain `grace run`
```

See [Creating a Bot](../guides/creating-a-bot.md#run-your-bot) for the full `grace run` walkthrough.
