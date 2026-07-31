import pytest

from grace.application import Application
from grace.exceptions import ConfigError


@pytest.fixture
def app():
    return Application()


def test_init_without_database_config(app):
    """Test if Application can be instantiated without a database.cfg"""
    assert app is not None


def test_has_database_without_database_config(app):
    """Test if has_database is False when no database is configured"""
    assert app.has_database is False


def test_database_exists_without_database_config(app):
    """Test if database_exists is False when no database is configured"""
    assert app.database_exists is False


def test_database_infos_without_database_config(app):
    """Test if database_infos is empty when no database is configured"""
    assert app.database_infos == {}


def test_load_database_without_database_config(app):
    """Test if load_database is a no-op when no database is configured"""
    app.load_database()


def test_create_database_without_database_config(app):
    """Test if create_database raises a clear error when no database is configured"""
    with pytest.raises(ConfigError):
        app.create_database()
