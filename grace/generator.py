from click import Command, Group
from pathlib import Path
from grace.importer import import_package_modules
from cookiecutter.main import cookiecutter
from grace.exceptions import ValidationError


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


class Generator(Command):
    """Base class for a generator command.

    This class provides a base implementation for a generator command that uses 
    Cookiecutter to generate a project template.
    """
    NAME: str = None
    OPTIONS: dict = {

    }

    def __init__(self):
        if not self.NAME:
            raise ValueError("Generator name must be defined.")

        super().__init__(self.NAME, callback=self._generate, **self.OPTIONS)

    @property
    def templates_path(self) -> Path:
        return Path(__file__).parent / 'generators' / 'templates'

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

    def generate_template(self, template: str, values: dict[str, any] = {}):
        """Generates a template using Cookiecutter.

        :param template: The name of the template to generate.
        :type template: str

        :param values: The values to pass to the template. (default is {})
        :type values: dict[str, any]
        """
        template_path = str(self.templates_path / template)
        cookiecutter(template_path, extra_context=values, no_input=True)
