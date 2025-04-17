"""This module provides a base implementation for a generator command,
which simplifies the creation of templates using Cookiecutter. It also provides
utilities for registering multiple generators to a command group dynamically.


Usage:

```python
from grace.generator import Generator


class MyGenerator(Generator):
    NAME = 'my_generator'

    def generate(self, *args, **kwargs):
        # Implement the generate method here
        ...


def generator() -> Generator:
    return MyGenerator()
```

"""
import inflect


from click import Command, Group
from pathlib import Path
from grace.application import Application
from grace.importer import import_package_modules
from grace.exceptions import GeneratorError, ValidationError, NoTemplateError
from cookiecutter.main import cookiecutter
from jinja2 import Environment, PackageLoader
from typing import Any


def register_generators(command_group: Group):
    """Registers generator commands to the given Click command group.

    This function dynamically imports all modules in the `grace.generators` package 
    and registers each module's `generator` command to the provided `command_group`.

    :param command_group: The Click command group to register the generators to.
    :type command_group: Group
    """
    from grace import generators

    for module in import_package_modules(generators, shallow=False):
        command_group.add_command(module.generator())


def _camel_case_to_space(value: str) -> str:
    """Jinja2 filter to converts a camel case string to a space separated string.

    :param value: The camel case string to convert.
    :type value: str

    :return: The space separated string.
    :rtype: str
    """
    import re
    return re.sub(r"(?<=[a-z])([A-Z])", r" \1", value)


class Generator(Command):
    """Base class for implementing a generator command.

    This class provides a foundation for defining generator commands that use
    Cookiecutter to generate project templates. It includes methods for template
    generation, validation, and argument handling.

    Attributes:
    - `NAME`: The name of the generator command (must be defined by subclasses).
    - `OPTIONS`: A dictionary of additional Click options for the command.
    """
    NAME: str | None = None
    OPTIONS: dict = {

    }

    def __init__(self):
        """Ensures that the `NAME` attribute is defined by the subclass.
        Registers the command with Click using the specified name and options.

        :raises GeneratorError: If the `NAME` attribute is not defined.
        """
        self.app: Application | None = None

        if not self.NAME:
            raise GeneratorError("Generator name must be defined.")

        super().__init__(self.NAME, callback=self._generate, **self.OPTIONS)

    @property
    def templates_path(self) -> Path:
        return Path(__file__).parent / 'generators' / 'templates'

    def invoke(self, ctx):
        self.app = ctx.obj.get("app")
        return super().invoke(ctx)

    def generate(self, *args, **kwargs):
        """Generates template.

        :param args: The positional arguments passed to the command.
        :param kwargs: The keyword arguments passed to the command

        :raises NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError

    def _generate(self, *args, **kwargs):
        if not self.validate(*args, **kwargs):
            raise ValidationError("Validation failed.")
        self.generate(*args, **kwargs)

    def validate(self, *args, **kwargs):
        """Validates the arguments passed to the command."""
        return True

    def generate_template(self, template_dir: str, variables: dict[str, Any] = {}):
        """Generates a template using Cookiecutter.

        :param template_dir: The name of the template to generate.
        :type template_dir: str

        :param variables: The variables to pass to the template. (default is {})
        :type variables: dict[str, Any]
        """
        template = str(self.templates_path / template_dir)
        cookiecutter(template, extra_context=variables, no_input=True)

    def generate_file(
        self,
        template_dir: str,
        variables: dict[str, Any] = {},
        output_dir: str = ""
    ):
        """Generate a module using jinja2 template.

        :param template_dir: The name of the template to generate.
        :type template_dir: str

        :param variables: The variables to pass to the template. (default is {})
        :type variables: dict[str, Any]

        :param output_dir: The output directory for the generated template. (default is None)
        :type output_dir: str
        """
        env = Environment(
            loader=PackageLoader('grace', str(self.templates_path / template_dir)),
            extensions=['jinja2_strcase.StrcaseExtension']
        )

        env.filters['camel_case_to_space'] = _camel_case_to_space
        env.filters['pluralize'] = lambda w: inflect.engine().plural(w)

        if not env.list_templates():
            raise NoTemplateError(f"No templates found in {template_dir}")

        template_file = env.list_templates()[0]
        template = env.get_template(template_file)

        rendered_filename = env.from_string(template_file).render(variables)
        rendered_content = template.render(variables)

        with open(f"{output_dir}/{rendered_filename}", "w") as file:
            file.write(rendered_content)
