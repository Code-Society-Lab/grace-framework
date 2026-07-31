import logging
from unittest.mock import MagicMock

import pytest

from grace.cli import _load_database, _require_database, _show_application_info


@pytest.fixture
def app():
    return MagicMock(
        environment="development",
        command_sync=True,
        watch=False,
    )


def test_require_database_without_database__expect_false(app, caplog):
    app.has_database = False

    assert _require_database(app) is False
    assert "no database configured" in caplog.text.lower()


def test_require_database_with_database__expect_true(app, caplog):
    app.has_database = True

    assert _require_database(app) is True
    assert caplog.text == ""


def test_load_database_without_database__expect_no_create(app):
    app.has_database = False

    _load_database(app)

    app.create_database.assert_not_called()


def test_load_database_with_missing_database__expect_create_called(app):
    app.has_database = True
    app.database_exists = False

    _load_database(app)

    app.create_database.assert_called_once()


def test_load_database_with_existing_database__expect_create_not_called(app):
    app.has_database = True
    app.database_exists = True

    _load_database(app)

    app.create_database.assert_not_called()


def test_show_application_info_without_database__expect_no_database_line(app, caplog):
    app.has_database = False

    with caplog.at_level(logging.INFO):
        _show_application_info(app)

    assert "Using database" not in caplog.text


def test_show_application_info_with_database__expect_database_line(app, caplog):
    app.has_database = True
    app.database_infos = {"database": "grace.db", "dialect": "sqlite"}

    with caplog.at_level(logging.INFO):
        _show_application_info(app)

    assert "Using database: grace.db with sqlite" in caplog.text
