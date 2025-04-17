import pytest
from unittest.mock import patch, MagicMock
from grace.generator import Generator
from grace.exceptions import ValidationError
from grace.generator import register_generators


class MockGenerator(Generator):
    NAME = 'mock'


@pytest.fixture
def generator():
    return MockGenerator()


def test_generator(generator):
    """Test if the generator is initialized correctly"""
    assert generator.NAME == 'mock'
    assert generator.OPTIONS == {}


def test_validate(generator):
    """Test if the generator validate method returns True"""
    assert generator.validate() == True


def test_generate_template(generator):
    """Test if the generator generate_template method calls cookiecutter with the correct arguments"""
    with patch('grace.generator.cookiecutter') as cookiecutter:
        generator.generate_template('project', variables={})
        template_path = str(generator.templates_path / 'project')
        
        cookiecutter.assert_called_once_with(
            template_path,
            extra_context={},
            no_input=True
        )


def test_generate(generator):
    """Test if the generator generate method raises a NotImplementedError"""
    with pytest.raises(NotImplementedError):
        generator.generate()


def test_register_generators():
    """Test if the register_generators function registers all the generators"""
    with patch('grace.generator.import_package_modules') as import_package_modules:
        command_group = MagicMock()
        import_package_modules.return_value = [MagicMock(generator=MagicMock())]

        register_generators(command_group)
        command_group.add_command.assert_called_once()
        import_package_modules.assert_called_once()

        from grace import generators
        import_package_modules.assert_called_with(generators, shallow=False)


def test_generate_validate(generator):
    """Test if the generator _generate method raises a ValidationError"""
    with patch('grace.generator.Generator.validate') as validate:
        validate.return_value = False
    
        with pytest.raises(ValidationError):
            generator._generate()
            validate.assert_called_once()
