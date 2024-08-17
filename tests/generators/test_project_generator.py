import unittest
from unittest.mock import patch
from grace.generators.project_generator import ProjectGenerator

class TestProjectGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ProjectGenerator()

    @patch("builtins.print")
    @patch("grace.generator.Generator.generate_template")
    def test_generate_with_database(self, generate_template_mock, mock_print):
        """Test the generate method with database=True"""
        name = "example-project"

        self.generator.generate(name, database=True)

        mock_print.assert_called_once_with(f"Creating '{name}'")

        generate_template_mock.assert_called_once_with(
            "project",
            values={
                "project_name": name,
                "project_description": "",
                "database": "yes",
            }
        )

    @patch("grace.generator.Generator.generate_template")
    def test_generate_without_database(self, generate_template_mock):
        """Test the generate method with database=False"""
        name = "example-project"

        self.generator.generate(name, database=False)

        generate_template_mock.assert_called_once_with(
            "project",
            values={
                "project_name": name,
                "project_description": "",
                "database": "no",
            }
        )

    def test_validate_valid_name(self):
        """Test the validate method with a valid name"""
        name = "example-project"

        result = self.generator.validate(name)

        self.assertTrue(result)

    def test_validate_invalid_name(self):
        """Test the validate method with an invalid name"""
        name = "Example Project"

        with self.assertRaises(ValueError):
            self.generator.validate(name)

    @patch("builtins.print")
    @patch("grace.generator.Generator.generate_template")
    def test_generate_prints_correct_message(self, generate_template_mock, mock_print):
        """Test that the correct message is printed when generate is called"""
        name = "example-project11"

        self.generator.generate(name, database=True)
        mock_print.assert_called_once_with(f"Creating '{name}'")


if __name__ == "__main__":
    unittest.main()