from grace.application import Application


def _create_bot(app):
    """Factory to create the bot instance.

    Import is deferred to avoid circular dependency.
    """
    from bot.{{ cookiecutter.__project_slug }} import {{ cookiecutter.__project_class }}
    return {{ cookiecutter.__project_class }}(app)


app = Application()
bot = _create_bot(app)