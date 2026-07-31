from unittest.mock import MagicMock

import pytest

from grace.generators.migration_generator import MigrationGenerator


@pytest.fixture
def generator():
    generator = MigrationGenerator()
    generator.app = MagicMock(has_database=True)
    return generator


def test_generate_without_app__expect_value_error(generator):
    generator.app = None

    with pytest.raises(ValueError):
        generator.generate("Add Greeting model")


def test_generate_without_database__expect_warning_and_no_migration(
    mocker, generator, caplog
):
    generator.app.has_database = False
    mock_generate_migration = mocker.patch(
        "grace.generators.migration_generator.generate_migration"
    )

    generator.generate("Add Greeting model")

    mock_generate_migration.assert_not_called()
    assert "no database configured" in caplog.text.lower()


def test_generate_with_database__expect_migration_generated(mocker, generator):
    mock_generate_migration = mocker.patch(
        "grace.generators.migration_generator.generate_migration"
    )

    generator.generate("Add Greeting model")

    mock_generate_migration.assert_called_once_with(generator.app, "Add Greeting model")
