from grace.generator import Generator
from re import match
from logging import info


class ProjectGenerator(Generator):
    NAME = 'project'
    OPTIONS = {
        "hidden": True
    }

    def generate(self, name, database=True):
        info(f"Creating '{name}'")

        self.generate_template(self.NAME, values={
            "project_name": name,
			"project_description": "",
			"database": "yes" if database else "no"
        })

    def validate(self, name, **_kwargs):
        return match('([a-z]|[0-9]|-)+', name)


def generator():
    return ProjectGenerator()