from unittest.mock import MagicMock

import pytest

from grace.generator import Generator
from grace.generators.model_generator import ModelGenerator


@pytest.fixture
def generator():
    generator = ModelGenerator()
    generator.app = MagicMock(has_database=True)
    return generator


def test_generate_without_app__expect_value_error(generator):
    generator.app = None

    with pytest.raises(ValueError):
        generator.generate("Greeting", ("message:String",))


def test_generate_without_database__expect_no_file_and_warning(
    mocker, generator, caplog
):
    generator.app.has_database = False
    mock_generate_file = mocker.patch.object(Generator, "generate_file")

    generator.generate("Greeting", ("message:String",))

    mock_generate_file.assert_not_called()
    assert "no database configured" in caplog.text.lower()


def test_generate_with_database__expect_model_file_and_migration_generated(
    mocker, generator
):
    mock_generate_file = mocker.patch.object(Generator, "generate_file")
    mock_generate_migration = mocker.patch(
        "grace.generators.model_generator.generate_migration"
    )

    generator.generate("Greeting", ("message:String",))

    mock_generate_file.assert_called_once()
    mock_generate_migration.assert_called_once_with(generator.app, "Create Greeting")
