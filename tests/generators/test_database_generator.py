import pytest

from grace.generator import Generator
from grace.generators.database_generator import DatabaseGenerator


@pytest.fixture
def generator():
    return DatabaseGenerator()


def test_generate__expect_database_template_rendered(mocker, generator, tmp_path):
    mock_generate_template = mocker.patch.object(Generator, "generate_template")
    output_dir = str(tmp_path / "example-project")

    generator.generate(output_dir=output_dir)

    mock_generate_template.assert_called_once_with("database", output_dir=output_dir)


def test_generate__expect_config_files_copied(mocker, generator, tmp_path):
    mocker.patch.object(Generator, "generate_template")
    output_dir = str(tmp_path / "example-project")

    generator.generate(output_dir=output_dir)

    alembic_ini = tmp_path / "example-project" / "alembic.ini"
    database_cfg = tmp_path / "example-project" / "config" / "database.cfg"

    assert alembic_ini.exists()
    assert database_cfg.exists()
    assert "script_location = db/alembic/" in alembic_ini.read_text()
    assert "[database.development]" in database_cfg.read_text()


def test_database_generator__expect_name_and_empty_options(generator):
    assert generator.NAME == "database"
    assert generator.OPTIONS == {}


def test_validate__expect_true(generator):
    assert generator.validate() is True
