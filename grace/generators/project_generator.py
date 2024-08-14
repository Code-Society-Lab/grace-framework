from grace.generator import Generator


class ProjectGenerator(Generator):
    NAME = 'project'
    OPTIONS = {
        "hidden": True
    }

    def generate(self, name, database=True):
		# name must be `lower case separated by -`
        print(f"Creating '{name}'")

        self.generate_template(self.NAME, values={
            "project_name": name,
			"project_description": "",
			"database": "yes" if database else "no"
        })

    def validate(self, name, **_kwargs):
        # raise error if name isn't properly formated
        return True


generator = ProjectGenerator()
