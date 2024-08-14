import os, shutil


options = {
	"db": "{{ cookiecutter.database }}"
}

for folder, value in options.items():
	if value == "no":
		path = folder.strip()

		if path and os.path.exists(path):
			shutil.rmtree(path)
