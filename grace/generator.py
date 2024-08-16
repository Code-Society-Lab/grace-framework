from click import Command
from pathlib import Path
from grace.importer import import_package_modules
from cookiecutter.main import cookiecutter
from grace.exceptions import ValidationError


def register_generators(command_group):
    from grace import generators

    for module in import_package_modules(generators, shallow=False):
        command_group.add_command(module.generator)


class Generator(Command):
    NAME = None
    OPTIONS = {

    }

    def __init__(self):
        super().__init__(self.NAME, callback=self._generate, **self.OPTIONS)

    @property
    def templates_path(self):
        return Path(__file__).parent / 'generators' / 'templates'

    def generate(self, *args, **kwargs):
        raise NotImplementedError

    def _generate(self, *args, **kwargs):
        if not self.validate(*args, **kwargs):
            raise ValidationError()
        self.generate(*args, **kwargs)

    def validate(self, *args, **kwargs):
        return True

    def generate_template(self, template, values={}):
        template_path = str(self.templates_path / template)
        cookiecutter(template_path, extra_context=values, no_input=True)
