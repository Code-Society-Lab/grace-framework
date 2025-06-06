from os import path
from re import match
from ast import literal_eval
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from typing import MutableMapping, Mapping, Optional, Union
from configparser import ConfigParser, BasicInterpolation, NoOptionError, SectionProxy


class EnvironmentInterpolation(BasicInterpolation):
    """Interpolation which expands environment variables in values.

    With this literal '${NAME}', the config will process the value from the given
    environment variable and use it as it's value in the config.

    This includes exported environment variable (ex. 'export MY_VAR=...') and
    variable in '.env' files.

    Usage example.
        token = ${MY_SECRET_VAR}

    In the example above, token will take the value of the environment variable
    called 'MY_SECRET_VAR'. In case 'MY_SECRET_VAR' doesn't exist, the value will
    not be evaluated.
    """

    def before_get(
            self,
            parser: MutableMapping[str, Mapping[str, str]],
            section: str,
            option: str,
            value: str,
            defaults: Mapping[str, str]
    ) -> str:
        """Interpolate the value before getting it from the parser.

        :param parser: The parser to get the value from.
        :type parser: MutableMapping[str, Mapping[str, str]]
        :param section: The section to get the value from.
        :type section: str
        :param option: The option to get the value from.
        :type option: str
        :param value: The value to interpolate.
        :type value: str
        :param defaults: The default values to use.
        """
        value = super().before_get(parser, section, option, value, defaults)
        expandvars: str = path.expandvars(value)

        if (value.startswith("${") and value.endswith("}")) and value == expandvars:
            try:
                return str(parser.get(section, value))
            except NoOptionError:
                return ""
        return expandvars


class Config:
    """This class is the application configurations.
    It loads all the configuration for the given environment

    The config environment is chosen by checking the value of the `BOT_ENV`
    environment variable. If the variable is not set it will load
    with production by default.

    There can be only one config loaded at once. Which means thar if you
    instantiate a second or multiple Config object, they will all share the
    same environment. This is to say, that the config objects are identical.
    """
    def __init__(self) -> None:
        load_dotenv(".env")

        self.__environment: Optional[str] = None
        self.__config: ConfigParser = ConfigParser(
            interpolation=EnvironmentInterpolation()
        )

        self.read("config/settings.cfg")
        self.read("config/database.cfg")
        self.read("config/environment.cfg")

    @property
    def database(self) -> SectionProxy:
        return self.__config[f"database.{self.__environment}"]

    @property
    def client(self) -> SectionProxy:
        return self.__config["client"]

    @property
    def environment(self) -> SectionProxy:
        return self.__config[str(self.__environment)]

    @property
    def current_environment(self) -> Optional[str]:
        return self.__environment

    @property
    def database_uri(self) -> Union[str, URL, None]:
        if self.database.get("url"):
            return self.database.get("url")

        return URL.create(
            self.database.get("adapter", "sqlite"),
            self.database.get("user"),
            self.database.get("password"),
            self.database.get("host"),
            self.database.getint("port"),
            self.database.get("database", self.database_name)
        )

    @property
    def database_name(self) -> str:
        return f"{self.client['name']}_{self.current_environment}"

    def read(self, file: str):
        """Read the configuration file."""
        self.__config.read(file)

    def get(self, section_key, value_key, fallback=None) -> Optional[Union[str, int, float, bool]]:
        """Get the value from the configuration file.

        :param section_key: The section key to get the value from.
        :type section_key: str
        :param value_key: The value key to get the value from.
        :type value_key: str
        :param fallback: The value to return if the value is not found (default: None).
        :type fallback: Optional[Union[str, int, float, bool]]
        """
        value: str = self.__config.get(
            section_key, value_key,
            fallback=fallback
        )

        if value and match(r"^[\d.]*$|^(?:True|False)*$", value):
            return literal_eval(value)
        return value

    def set_environment(self, environment: str):
        """Set the environment for the configuration.

        :param environment: The environment to set.
        :type environment: str
        """
        self.__environment = environment
