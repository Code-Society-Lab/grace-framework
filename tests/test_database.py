from unittest.mock import MagicMock

import pytest

from grace.database import generate_migration
from grace.exceptions import ConfigError


def test_generate_migration_without_database__expect_config_error():
    app = MagicMock(has_database=False)

    with pytest.raises(ConfigError):
        generate_migration(app, "Add Greeting model")


def test_generate_migration_with_database__expect_revision_called(mocker):
    app = MagicMock(has_database=True, environment="development")
    mock_revision = mocker.patch("grace.database.revision")
    mocker.patch("grace.database.Config")

    generate_migration(app, "Add Greeting model")

    mock_revision.assert_called_once()
