from unittest.mock import MagicMock

import pytest

from grace.exceptions import ValidationError
from grace.generator import Generator
from grace.generators.model_generator import ModelGenerator


@pytest.fixture
def generator():
    generator = ModelGenerator()
    generator.app = MagicMock(has_database=True)
    return generator


def test_extract_columns_with_supported_types__expect_python_annotations(generator):
    columns, types = generator.extract_columns(("message:String", "age:Integer"))

    assert columns == [("message", "str"), ("age", "int")]
    assert types == ["str", "int"]


def test_extract_columns_with_unsupported_type__expect_validation_error(generator):
    with pytest.raises(ValidationError, match="Unsupported column type 'DateTime'"):
        generator.extract_columns(("created_at:DateTime",))


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


def test_generate__expect_model_file_with_python_type_annotations(mocker, generator):
    mock_generate_file = mocker.patch.object(Generator, "generate_file")
    mocker.patch("grace.generators.model_generator.generate_migration")

    generator.generate("Greeting", ("message:String",))

    mock_generate_file.assert_called_once()
    variables = mock_generate_file.call_args.kwargs["variables"]
    assert list(variables["model_columns"]) == ["message: str"]
    assert variables["model_column_types"] == ["str"]


def test_generate__expect_migration_generated(mocker, generator):
    mocker.patch.object(Generator, "generate_file")
    mock_generate_migration = mocker.patch(
        "grace.generators.model_generator.generate_migration"
    )

    generator.generate("Greeting", ("message:String",))

    mock_generate_migration.assert_called_once_with(generator.app, "Create Greeting")


def test_validate_valid_name__expect_true(generator):
    assert generator.validate("Greeting")


def test_validate_invalid_name__expect_false(generator):
    assert not generator.validate("greeting")
