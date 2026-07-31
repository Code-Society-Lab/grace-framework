# Writing Generators

`grace generate cog`, `grace generate model`, `grace generate migration`, and `grace generate project` (used internally by `grace new`) are all built on the same extension point: [`grace.generator.Generator`](../reference/generator.md). Any module you drop into `grace/generators/`, or into your own package registered the same way, that exposes a module-level `generator()` function is automatically discovered and added under `grace generate <NAME>`.

## Anatomy of a Generator

```python
from grace.generator import Generator


class MyGenerator(Generator):
    NAME = "my_generator"

    def generate(self, *args, **kwargs):
        # Implement the generate method here
        ...


def generator() -> Generator:
    return MyGenerator()
```

- `NAME` becomes the subcommand name: `grace generate my_generator`.
- `generate()` does the actual work and is called after `validate()` passes.
- `validate()` (optional) returns `False` to reject the arguments before `generate()` runs; a failed validation raises `ValidationError`.
- `OPTIONS` lets you customize the underlying [`click.Command`](https://click.palletsprojects.com/) — most commonly to declare positional arguments.
- Inside `generate()`/`validate()`, `self.app` gives you the current [`Application`](../reference/application.md) instance.

## Example: A Real Generator

Here's the actual `CogGenerator` (`grace/generators/cog_generator.py`), which backs `grace generate cog`:

```python
from logging import info
from re import match

from click.core import Argument
from jinja2_strcase.jinja2_strcase import to_snake

from grace.generator import Generator


class CogGenerator(Generator):
    NAME: str = "cog"
    OPTIONS: dict = {
        "params": [
            Argument(["name"], type=str),
            Argument(["description"], type=str, required=False, default=""),
        ],
    }

    def generate(self, name: str, description: str = ""):
        info(f"Creating cog '{name}'")

        self.generate_file(
            self.NAME,
            variables={
                "cog_name": name,
                "cog_module_name": to_snake(name),
                "cog_description": description,
            },
            output_dir="bot/extensions",
        )

    def validate(self, name: str, **_kwargs) -> bool:
        """A valid cog name must be PascalCase (letters and numbers only)."""
        return bool(match(r"^[A-Z][a-zA-Z0-9]*$", name))


def generator() -> Generator:
    return CogGenerator()
```

## Rendering Output

`Generator` gives you two ways to produce files, both rooted at `grace/generators/templates/`:

- **`generate_file(template_dir, variables, output_dir)`** — renders a single [Jinja2](https://jinja.palletsprojects.com/) template file (used by `cog` and `model`). The template directory's file is expected to be named with Jinja2 syntax too (e.g. `{{ cog_module_name }}_cog.py`), so both the filename and the contents get rendered from `variables`. Two extra filters are available: `camel_case_to_space` and `pluralize` (via [`jinja2-strcase`](https://pypi.org/project/jinja2-strcase/) and [`inflect`](https://pypi.org/project/inflect/)).
- **`generate_template(template_dir, variables)`** — runs an entire directory through [Cookiecutter](https://cookiecutter.readthedocs.io/) (used by `project`), for scaffolding multi-file/multi-directory output.

## Registration

Generators are discovered by [`register_generators`](../reference/generator.md), which is called automatically whenever `grace` starts inside a project (or before `grace new`, for the bare CLI). It imports every module under `grace.generators` and registers whatever `generator()` returns onto the `generate` command group.

!!! note
    `Generator.templates_path` always resolves to `grace/generators/templates/` inside the **installed** `grace` package — both `generate_file` and `generate_template` render from there. This means a new generator, and its templates, currently need to live inside the `grace` package itself (i.e. contributed to the framework), rather than dropped into an individual bot project. See the [Custom Generator example](../examples/custom-generator.md) for what that looks like in practice.

## Next Steps

Browse the [Reference](../reference/generator.md) section for the full `Generator` API, or look at the [Custom Generator example](../examples/custom-generator.md) for a complete, runnable generator.
