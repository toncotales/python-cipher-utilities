import sys
import unittest
from io import StringIO
from unittest.mock import patch

from password_generator import PasswordGenerator, main


class TestPasswordGeneratorInitialization(unittest.TestCase):
    """Tests for PasswordGenerator initialization and configuration."""

    def test_default_initialization(self):
        gen = PasswordGenerator()
        self.assertEqual(gen.default_length, 16)
        self.assertFalse(gen.include_all_symbols)
        self.assertEqual(gen.uncommon_characters, PasswordGenerator.DEFAULT_UNCOMMON)

    def test_invalid_length_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            PasswordGenerator(default_length=5)
        self.assertIn("Password length must be at least 8 characters", str(ctx.exception))

    def test_custom_uncommon_symbols(self):
        custom = {'!', '@'}
        gen = PasswordGenerator(custom_uncommon=custom)
        self.assertEqual(gen.uncommon_characters, custom)


class TestPasswordGeneratorGenerate(unittest.TestCase):
    """Tests for password generation logic and complexity constraints."""

    def setUp(self):
        self.gen = PasswordGenerator()

    def test_generate_default_length(self):
        password = self.gen.generate()
        self.assertEqual(len(password), 16)
        self.assertTrue(PasswordGenerator.is_strong(password))

    def test_generate_custom_length(self):
        password = self.gen.generate(length=24)
        self.assertEqual(len(password), 24)
        self.assertTrue(PasswordGenerator.is_strong(password))

    def test_generate_minimum_length(self):
        password = self.gen.generate(length=8)
        self.assertEqual(len(password), 8)
        self.assertTrue(PasswordGenerator.is_strong(password))

    def test_generate_invalid_length(self):
        with self.assertRaises(ValueError):
            self.gen.generate(length=7)

    def test_empty_symbol_pool_raises_value_error(self):
        # Pass all possible punctuation as uncommon characters
        all_punctuation = set(import_string_punctuation := "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
        gen = PasswordGenerator(custom_uncommon=all_punctuation)
        with self.assertRaises(ValueError) as ctx:
            gen.generate()
        self.assertIn("Allowed symbol pool is empty", str(ctx.exception))


class TestPasswordGeneratorStrengthValidation(unittest.TestCase):
    """Tests for is_strong static method validation rules."""

    def test_valid_strong_password(self):
        self.assertTrue(PasswordGenerator.is_strong("AAbb11!!"))

    def test_too_short_password(self):
        self.assertFalse(PasswordGenerator.is_strong("Ab1!"))

    def test_insufficient_uppercase(self):
        self.assertFalse(PasswordGenerator.is_strong("abb11!!A"))

    def test_insufficient_lowercase(self):
        self.assertFalse(PasswordGenerator.is_strong("AABB11!!"))

    def test_insufficient_digits(self):
        self.assertFalse(PasswordGenerator.is_strong("AAbb1!!@"))

    def test_insufficient_symbols(self):
        self.assertFalse(PasswordGenerator.is_strong("AAbb1134"))


class TestPasswordGeneratorCLI(unittest.TestCase):
    """Tests for CLI interaction via main()."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_generate_default(self, mock_stdout):
        test_args = ["password_generator.py"]
        with patch.object(sys, "argv", test_args):
            main()
        output = mock_stdout.getvalue().strip()
        self.assertEqual(len(output), 16)
        self.assertTrue(PasswordGenerator.is_strong(output))

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_validate_strong(self, mock_stdout):
        test_args = ["password_generator.py", "-v", "AAbb11!!"]
        with patch.object(sys, "argv", test_args):
            main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("[+] 'AAbb11!!' meets strength requirements.", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_validate_weak(self, mock_stdout):
        test_args = ["password_generator.py", "-v", "weakpass"]
        with patch.object(sys, "argv", test_args):
            main()
        output = mock_stdout.getvalue().strip()
        self.assertIn("[-] 'weakpass' fails strength requirements.", output)


if __name__ == "__main__":
    unittest.main()