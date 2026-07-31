# Application

The `Application` class is the core of every Grace bot. It manages configuration, the database engine and session, model discovery, extension discovery, and logging. Every generated project instantiates exactly one `Application` in `bot/__init__.py`, alongside the `Bot` that wraps it.

```python
from grace.application import Application

app = Application()
app.load()  # sets the environment and wires up logging, models, and the database
```

::: grace.application.Application
