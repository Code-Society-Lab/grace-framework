from grace.generator import Generator


class ProjectGenerator(Generator):
    NAME = 'project'
    OPTIONS = {
        "hidden": True
    }

    def generate(self, name, database=True) -> None:
        """Generate a new project.
        
        :param name: The name of the project.
        :type name: str
        :param database: Whether to include a database or not, defaults to True
        :type database: bool, optional
        """
		# name must be `lower case separated by -`
        print(f"Creating '{name}'")

        self.generate_template(self.NAME, values={
            "project_name": name,
			"project_description": "",
			"database": "yes" if database else "no"
        })

    def validate(self, name, **_kwargs) -> bool:
        """Validate the project name.
        
        :param name: The project name.
        :type name: str
        :raises ValueError: If the name is not in the correct format.
        :return: True if the name is valid.
        """
        if not name.islower() or '-' not in name:
            raise ValueError("Invalid name format. Name must be in lower case and separated by '-'")
        return True


generator = ProjectGenerator()
