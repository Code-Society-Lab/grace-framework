from grace.bot import Bot
from discord.ext.commands import Cog


class {{ cog_name | to_camel }}Cog(Cog, name="{{ cog_name | camel_case_to_space }}"{{ ', description="{}"'.format(cog_description) if cog_description }}):
	def __init__(self, bot: Bot):
		self.bot: Bot = bot


async def setup(bot: Bot):
	await bot.add_cog({{ cog_name }}Cog(bot))