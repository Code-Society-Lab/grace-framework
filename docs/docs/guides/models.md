# Models & Migrations

Models are how your bot talks to its database. Grace models are [`SQLModel`](https://sqlmodel.tiangolo.com/) classes with an ActiveRecord-style API layered on top by [`grace.model.Model`](../reference/model.md).

## Generating a Model

Generate your first model, in `column_name:Type` pairs:

```bash
grace generate model Task name:String description:String done:Boolean
```

This command automatically:

- Creates a new database migration in `db/alembic/versions/`
- Generates a new model class in `bot/models/task.py`
- Registers the model for use with the built-in ORM utilities

Example output:

```
[2025-10-18 21:02:21] development generate model_generator INFO Generating model 'Task'
[2025-10-18 21:02:21] development __init__ migration INFO Context impl SQLiteImpl.
[2025-10-18 21:02:21] development __init__ migration INFO Will assume non-transactional DDL.
[2025-10-18 21:02:21] development _compare_tables compare INFO Detected added table 'task'
Generating /db/alembic/versions/99e6d0cf0aec_create_task.py ...  done
```

!!! note
    Column types are SQLAlchemy-style names, not Python types: `String`, `Text`, `Integer`, `Float`, `Boolean`. Each is mapped to its corresponding Python annotation (`str`, `str`, `int`, `float`, `bool`) in the generated model. Any other type name raises a `ValidationError`.

!!! note
    `grace generate model` requires a database — if your project was created with `--no-database`, it warns and does nothing until you run `grace generate database` (see [Database Management](database.md#adding-a-database-later)).

The generated `bot/models/task.py`:

```python
from grace.model import Field, Model


class Task(Model):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    done: bool
```

You don't need to pass `table=True` yourself — Grace's model metaclass sets it automatically for every `Model` subclass.

## Database Migrations

Grace uses [Alembic](https://alembic.sqlalchemy.org/) to manage schema migrations. When you generate a model (or run `grace generate migration`), Grace autogenerates a migration by diffing your models against the current database schema, writing the result to `db/alembic/versions/`.

Example migration file:

```python
"""Create Task
Revision ID: 99e6d0cf0aec
Revises:
Create Date: 2025-10-18 21:02:21.978903
"""
import sqlmodel
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '99e6d0cf0aec'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('task')
```

Directory layout:

```
db/
├── alembic/
│   ├── versions/
│   │   └── 99e6d0cf0aec_create_task.py
│   ├── env.py
│   └── script.py.mako
```

### Writing a Migration Manually

If you change a model by hand (add a column, rename a field, etc.) without regenerating it, create a migration for just that change:

```bash
grace generate migration "Add priority to Task"
```

### Running Migrations

Apply pending migrations to your database:

```bash
grace db up
```

```
[2025-10-18 21:05:42] development db_up INFO Applying migration 99e6d0cf0aec_create_task.py
[2025-10-18 21:05:42] development db_up INFO Upgrade successful.
```

Roll back with `grace db down`. Both commands accept an optional revision (default `head`) — see [Database Management](database.md).

## Querying Models

Every `Model` subclass gets a fluent, chainable [`Query`](../reference/model.md) API directly on the class:

```python
from bot.models.task import Task

# Create
task = Task.create(name="Write docs", description="Finish the guide", done=False)

# Find
Task.find(1)                      # by primary key
Task.find_by(name="Write docs")   # first match by equality

# Query, filter, and order
Task.where(Task.done == False).order_by(Task.id.desc()).limit(10).all()
Task.not_(done=True).all()
Task.with_("comments").where(Task.done == True).all()

# Update / delete / reload
task.update(done=True)
task.reload()
task.delete()

# Aggregate
Task.count()
```

See the [`Model` reference](../reference/model.md) for the full list of query and persistence methods.

## Next Steps

Now let's expose these tasks to Discord users with [Extensions](extensions.md).
