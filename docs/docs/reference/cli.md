# CLI

The `grace` command (entry point `grace.cli:main`) is your interface to Grace Framework. Outside of a generated project, only `grace new` is available. Once inside a project (i.e. a directory containing an importable `bot` package), the full command set is available.

```bash
grace --help
```

## Global Options

Available on every in-project command (must come before the subcommand):

| Option | Description |
|---|---|
| `--environment TEXT` | The environment to load (`production`, `development`, `test`). Falls back to the `GRACE_ENV` environment variable, then `development`. |

```bash
grace --environment test db up
```

## Commands

### `grace new NAME`

Scaffolds a new bot project named `NAME` in a directory of the same name, via [`grace generate project`](../guides/generators.md). Available outside of a project.

### `grace run`

Runs the bot. Automatically creates the database if it doesn't exist.

| Option | Default | Description |
|---|---|---|
| `--sync / --no-sync` | `--sync` | Sync application (slash) commands on startup. |
| `--watch / --no-watch` | `--no-watch` | Enable hot reload — see [`Watcher`](watcher.md). |

```bash
grace run --watch
```

### `grace db`

Database management commands — see [Database Management](../guides/database.md) for details on each.

| Command | Arguments | Description |
|---|---|---|
| `grace db create` | — | Creates the database if it doesn't exist. |
| `grace db drop` | — | Drops all tables, then drops the database. |
| `grace db seed` | — | Runs `db/seed.py`'s `seed_database()`. |
| `grace db up [REVISION]` | `REVISION` (default `head`) | Applies migrations. |
| `grace db down [REVISION]` | `REVISION` (default `head`) | Reverts migrations. |

### `grace generate`

Scaffolding commands — see [Writing Generators](../guides/generators.md) for how these are registered, and [Models & Migrations](../guides/models.md#generating-a-model) / [Extensions](../guides/extensions.md#generating-a-cog) for usage.

| Command | Arguments | Description |
|---|---|---|
| `grace generate cog NAME [DESCRIPTION]` | `NAME` (PascalCase), `DESCRIPTION` (optional) | Generates `bot/extensions/<name>_cog.py`. |
| `grace generate model NAME [COLUMN:TYPE ...]` | `NAME` (PascalCase), variadic `COLUMN:TYPE` pairs | Generates `bot/models/<name>.py` and an initial migration. |
| `grace generate migration MESSAGE` | `MESSAGE` | Autogenerates an Alembic revision from the current model state. |
| `grace generate project NAME` | `NAME` (lowercase/hyphens) | Scaffolds a new project directory (used internally by `grace new`). |

`grace generate` is a dynamic command group — any module under `grace.generators` (or a package you register the same way) exposing a `generator()` function shows up here automatically.
