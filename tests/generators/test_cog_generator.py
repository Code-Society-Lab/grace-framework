import pytest
from grace.generator import Generator
from grace.generators.cog_generator import CogGenerator


@pytest.fixture
def generator():
    return CogGenerator()


def test_generate_cog(mocker, generator):
    """Test if the generate method creates the correct template with a database."""
    mock_generate_file = mocker.patch.object(Generator, 'generate_file')

    name = "Example"
    description = "This is an example cog."

    generator.generate(name, description)

    mock_generate_file.assert_called_once_with(
        'cog', 
        variables={
            'cog_name': name,
            'cog_description': description
        },
        output_dir="bot/extensions"
    )


def test_validate_valid_name(generator):
    """Test if the validate method passes for a valid project name."""
    valid_name = "CogExample"
    assert generator.validate(valid_name)


def test_validate_invalid_name(generator):
    """Test if the validate method raises ValueError for name without a hyphen."""
    assert not generator.validate("cog-example")
    assert not generator.validate("cog_example")
    assert not generator.validate("Cog-Example")
    assert not generator.validate("Cog_Example")
