from __future__ import annotations

import argparse
import random
import string
import sys


class InvalidModeError(ValueError):
    """Exception raised when an invalid shuffling mode is specified."""
    pass


class StringManipulator:
    """
    Utility for deterministic string shuffling, unshuffling, and ciphers.
    """
    
    def __init__(self, seed_value: int | None = None) -> None:
        """Initialize the manipulator with an optional RNG seed value."""
        self.seed_value = (
            seed_value
            if seed_value is not None
            else random.randint(0, 2**31)
        )
        self._rng = random.Random(self.seed_value)
        
    def reset_rng(self) -> None:
        """Reset the internal RNG back to its initial seed state."""
        self._rng = random.Random(self.seed_value)
        
    def pseudo_shuffle(self, text: str, mode: str = "fisher_yates") -> str:
        """Shuffle a string pseudo-randomly using the specified mode."""
        if not text:
            return text
        
        chars = list(text)
        n = len(chars)
        self.reset_rng()
        
        if mode == "fisher_yates":
            for i in range(n - 1, 0, -1):
                j = self._rng.randint(0, i)
                chars[i], chars[j] = chars[j], chars[i]
            return "".join(chars)
        
        elif mode == "sample":
            return "".join(self._rng.sample(chars, n))
        
        elif mode == "deterministic":
            current_seed = (
                self.seed_value if self.seed_value is not None else 1337
            )
            multiplier = 1664525
            increment = 1013904223
            modulus = 2**32
            
            for i in range(n - 1, 0, -1):
                current_seed = (multiplier * current_seed + increment) % modulus
                j = current_seed % (i + 1)
                chars[i], chars[j] = chars[j], chars[i]
            return "".join(chars)
        
        else:
            raise InvalidModeError(
                "Invalid mode. Choose 'fisher_yates', 'sample', "
                "or 'deterministic'."
            )
            
    def unshuffle_fisher_yates(self, shuffled_text: str) -> str:
        """Reverse a Fisher-Yates shuffle to restore original string."""
        if not shuffled_text:
            return shuffled_text
        
        chars = list(shuffled_text)
        n = len(chars)
        
        self.reset_rng()
        swap_indices = []
        for i in range(n - 1, 0, -1):
            j = self._rng.randint(0, i)
            swap_indices.append((i, j))
            
        for i, j in reversed(swap_indices):
            chars[i], chars[j] = chars[j], chars[i]
            
        return "".join(chars)
    
    def _generate_cipher_maps(self) -> tuple[dict[str, str], dict[str, str]]:
        """Generate encryption and decryption substitution maps from seed."""
        self.reset_rng()
        base_chars = [c for c in string.printable if c not in string.whitespace]
        shuffled_chars = base_chars.copy()
        
        self._rng.shuffle(shuffled_chars)
        encrypt_map = dict(zip(base_chars, shuffled_chars))
        decrypt_map = dict(zip(shuffled_chars, base_chars))
        return encrypt_map, decrypt_map
    
    def substitution_encrypt(self, text: str) -> str:
        """Encrypt string using a seed-generated substitution map."""
        encrypt_map, _ = self._generate_cipher_maps()
        return "".join(encrypt_map.get(char, char) for char in text)
    
    def substitution_decrypt(self, cipher_text: str) -> str:
        """Decrypt string using a seed-generated substitution map."""
        _, decrypt_map = self._generate_cipher_maps()
        return "".join(decrypt_map.get(char, char) for char in cipher_text)


def main() -> None:
    """Command-line interface entrypoint."""
    parser = argparse.ArgumentParser(
        description="String manipulation, pseudo-shuffling, and ciphers."
    )
    
    parser.add_argument(
        "action",
        choices=["shuffle", "unshuffle", "encrypt", "decrypt"],
        help="Action to perform on input text"
    )
    parser.add_argument(
        "text",
        type=str,
        help="Target input text string"
    )
    parser.add_argument(
        "-s", "--seed",
        type=int,
        default=42,
        help="Random Number Generator seed value (default: 42)"
    )
    parser.add_argument(
        "-m", "--mode",
        choices=["fisher_yates", "sample", "deterministic"],
        default="fisher_yates",
        help="Shuffling mode for shuffle action (default: fisher_yates)"
    )
    
    args = parser.parse_args()
    
    try:
        manipulator = StringManipulator(seed_value=args.seed)
        if args.action == "shuffle":
            result = manipulator.pseudo_shuffle(args.text, mode=args.mode)
        elif args.action == "unshuffle":
            result = manipulator.unshuffle_fisher_yates(args.text)
        elif args.action == "encrypt":
            result = manipulator.substitution_encrypt(args.text)
        elif args.action == "decrypt":
            result = manipulator.substitution_decrypt(args.text)
            
        print(f"Result: {result}")
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()