# Database

Thin wrappers around [Alembic](https://alembic.sqlalchemy.org/)'s `revision`, `upgrade`, and `downgrade` commands, scoped to the current `Application`'s environment and `alembic.ini`. These back the `grace generate migration` and `grace db up`/`grace db down` commands — see [Database Management](../guides/database.md).

::: grace.database
