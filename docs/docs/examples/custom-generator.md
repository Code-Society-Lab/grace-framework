# Custom Generator

`Generator.templates_path` resolves to `grace/generators/templates/` inside the installed `grace` package, so adding a new `grace generate <name>` command means contributing it to the framework itself — a new module under `grace/generators/` plus a template under `grace/generators/templates/`. This example walks through adding a `service` generator that scaffolds a plain helper class, following the same shape as the built-in [`CogGenerator`](../reference/generator.md).

## 1. Add a Template

`grace/generators/templates/service/{{ service_module_name }}.py`:

```python
class {{ service_name }}:
    def __init__(self):
        pass
```

## 2. Write the Generator

`grace/generators/service_generator.py`:

```python
from logging import info
from re import match

from click.core import Argument
from jinja2_strcase.jinja2_strcase import to_snake

from grace.generator import Generator


class ServiceGenerator(Generator):
    NAME: str = "service"
    OPTIONS: dict = {
        "params": [
            Argument(["name"], type=str),
        ],
    }

    def generate(self, name: str):
        info(f"Creating service '{name}'")

        self.generate_file(
            self.NAME,
            variables={
                "service_name": name,
                "service_module_name": to_snake(name),
            },
            output_dir="bot/helpers",
        )

    def validate(self, name: str, **_kwargs) -> bool:
        """A valid service name must be PascalCase."""
        return bool(match(r"^[A-Z][a-zA-Z0-9]*$", name))


def generator() -> Generator:
    return ServiceGenerator()
```

Because it lives directly under `grace/generators/`, `register_generators` picks it up automatically — no manual registration step.

## 3. Use It

```bash
grace generate service Notifier
```

Generates `bot/helpers/notifier.py`:

```python
class Notifier:
    def __init__(self):
        pass
```

## Validating Arguments

`validate()` runs before `generate()` and can reject bad input before any files are written — return `False` (or raise [`ValidationError`](../reference/exceptions.md)) and `_generate` raises `ValidationError` on your behalf. See [`tests/test_generator.py`](https://github.com/Code-Society-Lab/grace-framework/blob/main/tests/test_generator.py) in the repository for a minimal `Generator` subclass used in Grace's own test suite.
