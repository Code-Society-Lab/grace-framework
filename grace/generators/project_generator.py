from grace.generator import Generator
from grace.generators.database_generator import generator as db_generator
from re import match
from logging import info


class ProjectGenerator(Generator):
    NAME = 'project'
    OPTIONS = {
        "hidden": True
    }

    def generate(self, name: str, database: bool = True):
        info(f"Creating '{name}'")

        self.generate_template(self.NAME, variables={
            "project_name": name,
            "project_description": "",
            "database": database
        })

        if database:
            # Should probably be moved into its own generator so we can
            # generate add the database later on.
            db_generator().generate(output_dir=name)

    def validate(self, name: str, **_kwargs) -> bool:
        """Validate the project name.

        A valid project name must:
        - contain only lowercase letters, numbers, and hyphens

        Example:
        - "awesome-project" is valid
        - "awesomeproject" is valid
        - "awesome-project1" is valid
        - "my-awesome-project" is valid

        - "awesomeProject" is invalid
        - "AwesomeProject" is invalid
        - "awesome_project" is invalid
        - "myAwesomeproject12" is invalid
        """
        return bool(match('([a-z]|[0-9]|-)+', name))


def generator() -> Generator:
    return ProjectGenerator()
