# Configuration

Every generated bot ships with configuration files under `config/`, all read by [`Config`](../reference/config.md) and combined by [`Application`](../reference/application.md):

| File | Purpose |
|---|---|
| `config/settings.cfg` | Client identity (name, prefix, description, guild) and the Discord token |
| `config/database.cfg` | Per-environment database connection settings — only present if your project has a database |
| `config/environment.cfg` | Per-environment logging and SQLAlchemy echo settings |

`config/database.cfg` is optional: it's included by default when you run `grace new`, skipped with `--no-database`, and can be added later with `grace generate database` (see [Database Management](database.md#adding-a-database-later)). Without it, `Config.database`/`database_uri` return `None` and `Application.has_database` is `False`.

Grace uses three environments — `production`, `development`, and `test` — selected via the `GRACE_ENV` environment variable. If unset, `development` is used by default (see `Application.load`).

## Environment Variable Interpolation

Config values can reference environment variables (including ones loaded from a `.env` file) using `${NAME}` syntax. This is handled by [`EnvironmentInterpolation`](../reference/config.md):

```ini
token = ${DISCORD_TOKEN}
```

`DISCORD_TOKEN` is read from `.env` or the shell environment. If the variable isn't set, the value is left empty rather than raising an error.

## `settings.cfg`

```ini
[client]
name = task-bot
prefix = ::
description = task-bot
guild_id = ${GUILD_ID}

[discord]
; Although it is possible to set directly your discord token here, we recommend, for security reasons, that you set
; your discord token as an environment variable called 'DISCORD_TOKEN'.
token = ${DISCORD_TOKEN}
```

- `[client]` is exposed as `Bot.config` inside your bot (an alias for `app.client`) and is used to build the command prefix, description, and optional guild-restricted command sync.
- `[discord]` `token` is what `Application` reads on startup and exposes as `app.token`.

## `database.cfg`

```ini
[database.production]
url = ${DATABASE_URL}

[database.development]
adapter = sqlite
database = development.db

[database.test]
adapter = sqlite
database = test.db
```

Each section is named `database.<environment>`. You need at minimum an `adapter` (the SQL dialect, optionally `dialect+driver`, e.g. `postgresql+psycopg2`) and a `database` name — or a full `url` (as used for `production` above, letting you supply a complete SQLAlchemy connection string via an environment variable). Optional keys: `user`, `password`, `host`, `port`.

See the [SQLAlchemy dialects reference](https://docs.sqlalchemy.org/en/14/dialects/index.html) for supported adapters, and the [engine configuration guide](https://docs.sqlalchemy.org/en/14/core/engines.html) for further details.

## `environment.cfg`

```ini
[production]
log_level = INFO
sqlalchemy_echo = False

[development]
log_level = DEBUG
sqlalchemy_echo = True

[test]
log_level = ERROR
sqlalchemy_echo = True
```

`log_level` controls both the file logger (`logs/<environment>.log`) and the console logger. `sqlalchemy_echo` toggles SQL statement logging, which is useful while developing models and queries.

## Reading Config Values in Your Code

Anywhere you have access to `app.config` (a [`Config`](../reference/config.md) instance), you can read arbitrary values:

```python
guild_id = app.config.get("client", "guild_id")
```

`Config.get` automatically evaluates numeric, boolean, and list-looking values, so `guild_id = 123456789012345678` in your `.cfg` file comes back as an `int`, not a string.

## Next Steps

With configuration in place, move on to [Models & Migrations](models.md) to give your bot something to store.
