import pytest
from unittest.mock import call
from grace.generator import Generator
from grace.generators.project_generator import ProjectGenerator


@pytest.fixture
def generator():
    return ProjectGenerator()


def test_generate_project_with_database(mocker, generator):
    """Test if the generate method creates the correct template with a database."""
    mock_generate_template = mocker.patch.object(Generator, 'generate_template')
    name = "example-project"

    generator.generate(name, database=True)

    expected_calls = [
        call('project', variables={
            'project_name': name,
            'project_description': '',
            'database': True
        }),
        call('database', variables={
            'output_dir': name
        })
    ]

    mock_generate_template.assert_has_calls(expected_calls)
    assert mock_generate_template.call_count == 2


def test_generate_project_without_database(mocker, generator):
    """Test if the generate method creates the correct template without a database."""
    mock_generate_template = mocker.patch.object(Generator, 'generate_template')
    name = "example-project"
    
    generator.generate(name, database=False)

    mock_generate_template.assert_called_once_with('project', variables={
        'project_name': name,
        'project_description': '',
        'database': False
    })


def test_validate_valid_name(generator):
    """Test if the validate method passes for a valid project name."""
    valid_name = "example-project"
    assert generator.validate(valid_name) == True


def test_validate_invalid_name_no_hyphen(generator):
    """Test if the validate method raises ValueError for name without a hyphen."""
    invalid_name = "ExampleProject"
    assert generator.validate(invalid_name) == False


def test_validate_invalid_name_uppercase(generator):
    """Test if the validate method raises ValueError for uppercase name."""
    invalid_name = "Example-Project"
    assert generator.validate(invalid_name) == False

