from config.application import Application
from logging import info, warning, critical
from discord import LoginFailure

app = Application()


def start():
    """Starts the bot"""
    from bot.greeter import Greeter

    try:
        if app.token:
            bot = Greeter()
            bot.run(app.token)
        else:
            critical("Unable to find the token. Make sure your current directory contains an '.env' and that "
                     "'DISCORD_TOKEN' is defined")
    except LoginFailure as e:
        critical(f"Authentication failed : {e}")
