# Welcome to **Grace Framework**

Grace Framework is an opinionated, extensible Discord bot framework built on top of [discord.py](https://github.com/Rapptz/discord.py). It is designed to help developers rapidly build scalable, feature-rich Discord bots with minimal boilerplate.

#### Key Features
- Quick to start: generate a full-featured bot in seconds
- Modular architecture: clean separation of features via extensions (cogs)
- Database integration: connect your bot to a persistent backend with a single config
- Built-in generators: create extensions, models, and migrations with a single command

#### Inspiration

Grace Framework was inspired by the community Discord bot, [Grace](https://github.com/Code-Society-Lab/grace), that evolved into a modular and powerful bot — it began to resemble a standalone framework. Recognizing its potential, the developers extracted its architecture into Grace Framework, making its ease-of-use and flexibility available to other developers.

## What These Guides Cover

Throughout these guides, we build a bot called `task-bot` — a simple task manager. It will be able to:

- List all current tasks — `/list`
- Add new tasks — `/add <task name> <task description>`
- Remove existing tasks — `/delete <task id>`
- Mark tasks as complete — `/done <task id>`

Along the way you'll learn:

- [Installation](installation.md) — installing Grace Framework and its requirements
- [Creating a Bot](creating-a-bot.md) — scaffolding a project, the generated layout, and running your bot
- [Configuration](configuration.md) — how `config/*.cfg` files and environments work
- [Models & Migrations](models.md) — defining database models and evolving your schema with Alembic
- [Extensions](extensions.md) — organizing commands into cogs
- [Database Management](database.md) — creating, dropping, and seeding your database from the CLI
- [Writing Generators](generators.md) — extending `grace generate` with your own generators

## Quick Start

Install Grace Framework:
```bash
pip install grace-framework
```

Generate a new bot:
```bash
grace new task-bot
cd task-bot
```

Set your bot token in `.env`:
```
DISCORD_TOKEN=your token here
```

Run it:
```bash
grace run
```

For the full walkthrough — including models, migrations, and cogs — start with [Installation](installation.md).

## Resources

Here's a list of resources that might be useful when working with **Grace Framework**:

- [Python's Docs](https://docs.python.org/3/)
- [discord.py](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/docs/intro)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [Pytest](https://docs.pytest.org/)

## Contributing

We welcome any contributions, whether it's fixing bugs, suggesting features, or improving the docs — every bit helps:

- [Submit an issue](https://github.com/Code-Society-Lab/grace-framework/issues)
- [Open a pull request](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)
- Or hop into our [Discord community](https://discord.gg/code-society-823178343943897088) and say hi!

If you intend to contribute, please read the [CONTRIBUTING.md](https://github.com/Code-Society-Lab/grace-framework/blob/main/CONTRIBUTING.md) first. Additionally, **every contributor** is expected to follow the [code of conduct](https://github.com/Code-Society-Lab/grace-framework/blob/main/CODE_OF_CONDUCT.md).
