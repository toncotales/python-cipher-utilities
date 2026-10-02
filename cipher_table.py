from __future__ import annotations

import argparse
import string


class CipherTable:
    """A Vigenere-style substitution cipher table."""
    
    def __init__(self, characters: str) -> None:
        if not characters:
            raise ValueError("Character set cannot be empty.")
        if len(set(characters)) != len(characters):
            raise ValueError("Character set contains duplicate characters.")
        
        self.characters = characters
        self.num_chars = len(self.characters)
        self.char_to_index = {char: i for i, char in enumerate(self.characters)}
        self.index_to_char = {i: char for i, char in enumerate(self.characters)}
        self._table: list[str] | None = None
        
    @property
    def table(self) -> list[str]:
        """Lazy-generate shifted table rows only when accessed."""
        if self._table is None:
            self._table = [
                self.characters[i:] + self.characters[:i]
                for i in range(self.num_chars)
            ]
        return self._table
    
    def get_row(self, key_char: str) -> str | None:
        """Retrieve the shifted row for a specific key character."""
        if key_char in self.char_to_index:
            index = self.char_to_index[key_char]
            return self.table[index]
        return None
    
    def encrypt(self, plaintext: str, keyword: str) -> str:
        """Encrypt a plaintext string using a repeating keyword."""
        if not keyword:
            raise ValueError("Keyword cannot be empty.")
        if not all(c in self.char_to_index for c in keyword):
            raise ValueError("Keyword contains characters not in table.")
        
        ciphertext = []
        keyword_length = len(keyword)
        for i, plain_char in enumerate(plaintext):
            key_char = keyword[i % keyword_length]
            
            if plain_char in self.char_to_index:
                plain_index = self.char_to_index[plain_char]
                key_index = self.char_to_index[key_char]
                ciphertext_index = (plain_index + key_index) % self.num_chars
                ciphertext.append(self.index_to_char[ciphertext_index])
            else:
                ciphertext.append(plain_char)
                
        return "".join(ciphertext)
    
    def decrypt(self, ciphertext: str, keyword: str) -> str:
        """Decrypt a ciphertext string back into plaintext using the keyword."""
        if not keyword:
            raise ValueError("Keyword cannot be empty.")
        if not all(c in self.char_to_index for c in keyword):
            raise ValueError("Keyword contains characters not in table.")
        
        plaintext = []
        keyword_length = len(keyword)
        for i, cipher_char in enumerate(ciphertext):
            key_char = keyword[i % keyword_length]
            
            if cipher_char in self.char_to_index:
                cipher_index = self.char_to_index[cipher_char]
                key_index = self.char_to_index[key_char]
                plaintext_index = (
                    cipher_index - key_index + self.num_chars
                ) % self.num_chars
                plaintext.append(self.index_to_char[plaintext_index])
            else:
                plaintext.append(cipher_char)
                
        return "".join(plaintext)


def main() -> None:
    """Command-line interface entrypoint."""
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt text using a Vigenère-style cipher."
    )
    
    parser.add_argument(
        "action",
        choices=["encrypt", "decrypt"],
        help="Choose whether to encrypt or decrypt the text"
    )
    parser.add_argument(
        "text",
        type=str,
        help="The input text to be processed"
    )
    parser.add_argument(
        "-k", "--keyword",
        type=str,
        required=True,
        help="The secret keyword used for the cipher"
    )
    
    # Optional character set override
    # (defaults to a broad set of printable characters)
    default_chars = (
        string.ascii_letters + string.digits + string.punctuation + " "
    )
    parser.add_argument(
        "-c", "--chars",
        type=str,
        default=default_chars,
        help=(
            "Custom character set for the cipher table "
            "(default: standard printable characters)"
        )
    )
    
    args = parser.parse_args()
    
    try:
        cipher = CipherTable(args.chars)
        if args.action == "encrypt":
            result = cipher.encrypt(args.text, args.keyword)
            print(f"Encrypted text: {result}")
        elif args.action == "decrypt":
            result = cipher.decrypt(args.text, args.keyword)
            print(f"Decrypted text: {result}")
    except ValueError as err:
        parser.error(str(err))


if __name__ == "__main__":
    main()