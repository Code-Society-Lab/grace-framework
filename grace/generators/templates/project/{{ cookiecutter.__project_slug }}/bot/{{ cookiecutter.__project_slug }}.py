from grace.bot import Bot
from logging import info


class {{ cookiecutter.__project_class }}(Bot):
    async def on_ready(self):
        info(f"{self.user.name}:#{self.user.id} is online and ready to use!")