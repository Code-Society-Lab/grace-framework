# Database Management

Grace exposes a `grace db` command group for managing your bot's database, plus automatic database creation on startup.

## Create

```bash
grace db create
```

Creates the database itself (the file for SQLite, the schema for other dialects) if it doesn't already exist. This does **not** create tables — run [migrations](models.md#database-migrations) with `grace db up` for that. If the database already exists, this is a no-op with a warning.

!!! tip
    `grace run` automatically creates the database on startup if it's missing, so you rarely need to run `grace db create` yourself.

## Migrate

```bash
grace db up [REVISION]
grace db down [REVISION]
```

Applies (`up`) or reverts (`down`) Alembic migrations from `db/alembic/versions/`. `REVISION` defaults to `head`. See [Models & Migrations](models.md#database-migrations) for how migrations are generated.

## Seed

```bash
grace db seed
```

Imports `db/seed.py` from your project and calls `seed_database()`. This is a stub generated with your project — fill it in with whatever initial data your bot needs:

```python
# db/seed.py
from bot.models.task import Task

def seed_database():
    Task.create(name="Example task", description="Created by the seed script", done=False)
```

If you have multiple seed sources, consider organizing them under a `db/seeds/` directory and importing them from `seed_database()`.

## Drop

```bash
grace db drop
```

Drops all tables, then drops the database itself. If the database doesn't exist, this is a no-op with a warning.

!!! warning
    This is destructive and unrecoverable outside of your migrations/backups — use with care, especially against a shared database.

## Choosing an Environment

Every `grace` command inside a project accepts `--environment`, which selects the `[database.<environment>]` section from `config/database.cfg` (see [Configuration](configuration.md)):

```bash
grace --environment test db create
grace --environment test db up
```

If omitted, the `GRACE_ENV` environment variable is used, falling back to `development`.

## Next Steps

To extend `grace generate` with your own scaffolding commands, see [Writing Generators](generators.md).
