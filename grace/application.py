from configparser import SectionProxy

from coloredlogs import install
from logging import basicConfig, critical
from logging.handlers import RotatingFileHandler

from types import ModuleType
from typing import Generator, Any, Union, Dict, no_type_check

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    Session,
    DeclarativeMeta
)
from sqlalchemy_utils import (
    database_exists,
    create_database,
    drop_database
)
from pathlib import Path
from grace.config import Config
from grace.exceptions import ConfigError
from grace.importer import find_all_importables, import_module


ConfigReturn = Union[str, int, float, None]


class Application:
    """This class is the core of the application In other words,
    this class that manage the database, the application environment
    and loads the configurations.
    """

    __config: Union[Config, None] = None
    __session: Union[Session, None] = None
    __base: DeclarativeMeta = declarative_base()

    def __init__(self) -> None:
        database_config_path: Path = Path("config/database.cfg")
        
        if not database_config_path.exists():
            raise ConfigError("Unable to find the 'database.cfg' file.")

        self.__token: str = str(self.config.get("discord", "token"))
        self.__engine: Union[Engine, None] = None

        self.command_sync: bool = True
        self.watch: bool = False

    @property
    def base(self) -> DeclarativeMeta:
        return self.__base

    @property
    def token(self) -> str:
        return str(self.__token)

    @property
    @no_type_check
    def session(self) -> Session:
        """Instantiate the session for querying the database."""

        if not self.__session:
            session: sessionmaker = sessionmaker(bind=self.__engine)
            self.__session = session()

        return self.__session

    @property
    def config(self) -> Config:
        if not self.__config:
            self.__config = Config()

        return self.__config

    @property
    def client(self) -> SectionProxy:
        return self.config.client

    @property
    def extension_modules(self) -> Generator[str, Any, None]:
        """Generate the extensions modules"""
        from bot import extensions

        for module in find_all_importables(extensions):
            imported: ModuleType = import_module(module)

            if not hasattr(imported, "setup"):
                continue
            yield module

    @property
    def database_infos(self) -> Dict[str, str]:
        return {
            "dialect": self.session.bind.dialect.name,
            "database": self.session.bind.url.database
        }

    @property
    def database_exists(self):
        return database_exists(self.config.database_uri)

    def get_extension_module(self, extension_name) -> Union[str, None]:
        """Return the extension from the given extension name"""

        for extension in self.extension_modules:
            if extension == extension_name:
                return extension
        return None

    def load(self, environment: str):
        """
        Sets the environment and loads all the component of the application
        """
        self.environment: str = environment
        self.config.set_environment(environment)

        self.load_logs()
        self.load_models()
        self.load_database()

    def load_models(self):
        """Import all models in the `bot/models` package."""
        from bot import models

        for module in find_all_importables(models):
            import_module(module)

    def load_logs(self) -> None:
        file_handler: RotatingFileHandler = RotatingFileHandler(
            f"logs/{self.config.current_environment}.log",
            maxBytes=10000,
            backupCount=5
        )

        basicConfig(
            level=self.config.environment.get("log_level"),
            format="[%(asctime)s] %(funcName)s %(levelname)s %(message)s",
            handlers=[file_handler],
        )

        install(
            self.config.environment.get("log_level"),
            fmt="[%(asctime)s] %(programname)s %(funcName)s %(module)s %(levelname)s %(message)s",
            programname=self.config.current_environment,
        )

    def load_database(self):
        """Loads and connects to the database using the loaded config"""

        self.__engine = create_engine(
            self.config.database_uri,
            echo=self.config.environment.getboolean("sqlalchemy_echo")
        )

        if self.database_exists:
            try:
                self.__engine.connect()
            except OperationalError as e:
                critical(f"Unable to load the 'database': {e}")

    def unload_database(self):
        """Unloads the current database"""

        self.__engine = None
        self.__session = None

    def reload_database(self):
        """
        Reload the database. This function can be use in case
        there's a dynamic environment change.
        """

        self.unload_database()
        self.load_database()

    def create_database(self):
        """Creates the database for the current loaded config"""

        self.load_database()
        create_database(self.config.database_uri)

    def drop_database(self):
        """Drops the database for the current loaded config"""

        self.load_database()
        drop_database(self.config.database_uri)

    def create_tables(self):
        """Creates all the tables for the current loaded database"""

        self.load_database()
        self.base.metadata.create_all(self.__engine)

    def drop_tables(self):
        """Drops all the tables for the current loaded database"""

        self.load_database()
        self.base.metadata.drop_all(self.__engine)
