from grace.application import Application
from bot.{{ cookiecutter.__project_slug }} import {{ cookiecutter.__project_class }}

app = Application()
bot = {{ cookiecutter.__project_class }}(app)