# Config

`Config` loads and exposes your project's `config/*.cfg` files for the currently selected environment. See the [Configuration guide](../guides/configuration.md) for a walkthrough of `settings.cfg`, `database.cfg`, and `environment.cfg`.

```python
from grace.application import Application

app = Application()
app.load()

app.config.get("client", "guild_id")
app.config.database_uri
```

::: grace.config.Config

::: grace.config.EnvironmentInterpolation
