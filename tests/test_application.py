import pytest

from grace.application import Application
from grace.exceptions import ConfigError


@pytest.fixture
def app():
    return Application()


def test_init_without_database__expect_no_error(app):
    assert app is not None


def test_has_database_without_database__expect_false(app):
    assert app.has_database is False


def test_database_exists_without_database__expect_false(app):
    assert app.database_exists is False


def test_database_infos_without_database__expect_empty_dict(app):
    assert app.database_infos == {}


def test_load_database_without_database__expect_no_op(app):
    app.load_database()


def test_create_database_without_database__expect_config_error(app):
    with pytest.raises(ConfigError):
        app.create_database()
