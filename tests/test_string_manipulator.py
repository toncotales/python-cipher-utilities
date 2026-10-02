import sys
import unittest
from io import StringIO
from unittest.mock import patch

from string_manipulator import InvalidModeError, StringManipulator, main


class TestStringManipulatorInitialization(unittest.TestCase):
    """Tests for StringManipulator initialization and RNG resetting."""

    def test_default_initialization(self):
        manip = StringManipulator()
        self.assertIsInstance(manip.seed_value, int)
        self.assertGreaterEqual(manip.seed_value, 1)

    def test_custom_seed_initialization(self):
        manip = StringManipulator(seed_value=12345)
        self.assertEqual(manip.seed_value, 12345)

    def test_invalid_seed_type_raises_type_error(self):
        with self.assertRaises(TypeError) as ctx:
            StringManipulator(seed_value="not_an_int")  # type: ignore
        self.assertIn("Seed value must be an integer", str(ctx.exception))


class TestStringManipulatorShuffleAndUnshuffle(unittest.TestCase):
    """Tests for shuffling modes and Fisher-Yates unshuffling."""

    def setUp(self):
        self.manip = StringManipulator(seed_value=42)
        self.text = "HelloWorld123!"

    def test_fisher_yates_shuffle_and_unshuffle_roundtrip(self):
        shuffled = self.manip.pseudo_shuffle(self.text, mode="fisher_yates")
        self.assertNotEqual(self.text, shuffled)
        
        unshuffled = self.manip.unshuffle_fisher_yates(shuffled)
        self.assertEqual(self.text, unshuffled)

    def test_sample_shuffle_mode(self):
        shuffled = self.manip.pseudo_shuffle(self.text, mode="sample")
        self.assertEqual(sorted(self.text), sorted(shuffled))

    def test_deterministic_shuffle_mode(self):
        shuffled = self.manip.pseudo_shuffle(self.text, mode="deterministic")
        self.assertEqual(sorted(self.text), sorted(shuffled))

    def test_invalid_mode_raises_error(self):
        with self.assertRaises(InvalidModeError):
            self.manip.pseudo_shuffle(self.text, mode="invalid_mode")

    def test_empty_string_handling(self):
        self.assertEqual(self.manip.pseudo_shuffle(""), "")
        self.assertEqual(self.manip.unshuffle_fisher_yates(""), "")


class TestStringManipulatorSubstitutionCipher(unittest.TestCase):
    """Tests for substitution encryption and decryption."""

    def setUp(self):
        self.manip = StringManipulator(seed_value=100)
        self.text = "Hello World! 123"

    def test_encrypt_decrypt_roundtrip(self):
        encrypted = self.manip.substitution_encrypt(self.text)
        self.assertNotEqual(self.text, encrypted)
        
        decrypted = self.manip.substitution_decrypt(encrypted)
        self.assertEqual(self.text, decrypted)

    def test_whitespace_passthrough(self):
        encrypted = self.manip.substitution_encrypt("A B\tC\n")
        self.assertEqual(encrypted[1], " ")
        self.assertEqual(encrypted[3], "\t")
        self.assertEqual(encrypted[5], "\n")


class TestStringManipulatorCLI(unittest.TestCase):
    """Tests for main() CLI invocation."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_shuffle_and_unshuffle(self, mock_stdout):
        # Shuffle
        test_args_shuffle = ["string_manipulator.py", "shuffle", "Hello", "-s", "42"]
        with patch.object(sys, "argv", test_args_shuffle):
            main()
        shuffle_output = mock_stdout.getvalue().strip().replace("Result: ", "")
        mock_stdout.seek(0)
        mock_stdout.truncate(0)

        # Unshuffle
        test_args_unshuffle = ["string_manipulator.py", "unshuffle", shuffle_output, "-s", "42"]
        with patch.object(sys, "argv", test_args_unshuffle):
            main()
        unshuffle_output = mock_stdout.getvalue().strip()
        self.assertEqual(unshuffle_output, "Result: Hello")


if __name__ == "__main__":
    unittest.main()