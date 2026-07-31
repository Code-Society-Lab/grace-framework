# Generator

The base class for every `grace generate` subcommand, plus the discovery function that registers them. See [Writing Generators](../guides/generators.md) for a full guide.

```python
from grace.generator import Generator


class MyGenerator(Generator):
    NAME = "my_generator"

    def generate(self, *args, **kwargs):
        ...


def generator() -> Generator:
    return MyGenerator()
```

::: grace.generator.Generator

::: grace.generator.register_generators
