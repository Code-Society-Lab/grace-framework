from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("grace-framework")
except PackageNotFoundError:
    from grace._version import version as __version__

from discord.ext.commands import *
