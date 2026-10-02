import sys
import unittest
from io import StringIO
from unittest.mock import patch

from cipher_table import CipherTable, main


class TestCipherTableInitialization(unittest.TestCase):
    """Tests for CipherTable class initialization and edge cases."""

    def test_valid_initialization(self):
        chars = "ABCDEF"
        cipher = CipherTable(chars)
        self.assertEqual(cipher.characters, chars)
        self.assertEqual(cipher.num_chars, 6)

    def test_empty_character_set_raises_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            CipherTable("")
        self.assertIn("Character set cannot be empty", str(ctx.exception))

    def test_duplicate_characters_raise_value_error(self):
        with self.assertRaises(ValueError) as ctx:
            CipherTable("AABC")
        self.assertIn("Character set contains duplicate characters", str(ctx.exception))

    def test_table_lazy_generation(self):
        cipher = CipherTable("ABC")
        self.assertIsNone(cipher._table)
        
        # Accessing property should generate the shifted table
        expected_table = ["ABC", "BCA", "CAB"]
        self.assertEqual(cipher.table, expected_table)
        self.assertIsNotNone(cipher._table)

    def test_get_row(self):
        cipher = CipherTable("ABC")
        self.assertEqual(cipher.get_row("B"), "BCA")
        self.assertIsNone(cipher.get_row("Z"))


class TestCipherTableEncryptDecrypt(unittest.TestCase):
    """Tests for encrypt and decrypt methods."""

    def setUp(self):
        self.default_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.cipher = CipherTable(self.default_chars)

    def test_standard_encrypt_decrypt_roundtrip(self):
        plaintext = "HELLOWORLD"
        keyword = "KEY"
        
        ciphertext = self.cipher.encrypt(plaintext, keyword)
        self.assertNotEqual(plaintext, ciphertext)
        
        decrypted = self.cipher.decrypt(ciphertext, keyword)
        self.assertEqual(decrypted, plaintext)

    def test_empty_keyword_raises_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.cipher.encrypt("HELLO", "")
        self.assertIn("Keyword cannot be empty", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            self.cipher.decrypt("HELLO", "")
        self.assertIn("Keyword cannot be empty", str(ctx.exception))

    def test_invalid_keyword_character_raises_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.cipher.encrypt("HELLO", "KEY123")
        self.assertIn("Keyword contains characters not in table", str(ctx.exception))

    def test_passthrough_unsupported_characters(self):
        """Characters not in character set should remain untouched."""
        plaintext = "HELLO WORLD!"
        keyword = "KEY"
        
        # ' ' and '!' are not in self.default_chars
        ciphertext = self.cipher.encrypt(plaintext, keyword)
        self.assertEqual(ciphertext[5], " ")
        self.assertEqual(ciphertext[11], "!")

        decrypted = self.cipher.decrypt(ciphertext, keyword)
        self.assertEqual(decrypted, plaintext)


class TestCipherTableCLI(unittest.TestCase):
    """Tests for command-line interface execution via main()."""

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_encrypt(self, mock_stdout):
        test_args = ["cipher_table.py", "encrypt", "Hello World", "-k", "SECRET"]
        with patch.object(sys, "argv", test_args):
            main()
        
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Encrypted text: :IN2SS}ST2H")

    @patch("sys.stdout", new_callable=StringIO)
    def test_cli_decrypt(self, mock_stdout):
        test_args = ["cipher_table.py", "decrypt", ":IN2SS}ST2H", "-k", "SECRET"]
        with patch.object(sys, "argv", test_args):
            main()
        
        output = mock_stdout.getvalue().strip()
        self.assertEqual(output, "Decrypted text: Hello World")


if __name__ == "__main__":
    unittest.main()