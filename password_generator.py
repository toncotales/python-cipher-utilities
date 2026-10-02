from __future__ import annotations

import argparse
import secrets
import string
import sys


class PasswordGenerator:
    """
    A modular class for generating and validating
    cryptographically secure passwords.
    """
    
    # Default set of uncommon or confusing symbols to exclude
    DEFAULT_UNCOMMON = {
        '[', ']', '{', '}', '<', '>', '(', ')',
        '\\', '/', ':', ';',
        '"', "'", '`',
        ',', '=', '%', '~'
    }
    
    def __init__(
        self,
        default_length: int = 16,
        include_all_symbols: bool = False,
        custom_uncommon: set[str] | None = None
    ) -> None:
        
        if default_length < 8:
            raise ValueError("Password length must be at least 8 characters.")
        
        self.default_length = default_length
        self.include_all_symbols = include_all_symbols
        if custom_uncommon is not None:
            self.uncommon_characters = custom_uncommon
        else:
            self.uncommon_characters = self.DEFAULT_UNCOMMON
        
    def _get_allowed_symbols(self) -> str:
        """Internal helper to build the allowed symbol pool."""
        if self.include_all_symbols:
            return string.punctuation
        return "".join(
            i for i in string.punctuation if i not in self.uncommon_characters
        )
        
    @staticmethod
    def _secure_shuffle(chars: list[str]) -> list[str]:
        """
        Cryptographically secure Fisher-Yates shuffle
        to break character positional bias.
        """
        shuffled = chars.copy()
        secrets.SystemRandom().shuffle(shuffled)
        return shuffled
    
    def generate(self, length: int | None = None) -> str:
        """Generates a cryptographically secure random password."""
        target_length = length if length is not None else self.default_length
        if target_length < 8:
            raise ValueError("Password length must be at least 8 characters.")
        
        symbols = self._get_allowed_symbols()
        if not symbols:
            raise ValueError(
                "Allowed symbol pool is empty. "
                "Cannot generate required symbols."
            )
        
        upper = string.ascii_uppercase
        lower = string.ascii_lowercase
        digits = string.digits
        
        # Seed guaranteed minimum character types
        password_chars = [
            secrets.choice(upper), secrets.choice(upper),
            secrets.choice(lower), secrets.choice(lower),
            secrets.choice(digits), secrets.choice(digits),
            secrets.choice(symbols), secrets.choice(symbols)
        ]
        
        all_pool = upper + lower + digits + symbols
        while len(password_chars) < target_length:
            password_chars.append(secrets.choice(all_pool))
            
        shuffled_chars = self._secure_shuffle(password_chars)
        return "".join(shuffled_chars)
    
    @staticmethod
    def is_strong(password: str) -> bool:
        """Validates if a password meets the high-complexity rules."""
        if len(password) < 8:
            return False
        
        has_upper = sum(1 for c in password if c.isupper()) >= 2
        has_lower = sum(1 for c in password if c.islower()) >= 2
        has_digit = sum(1 for c in password if c.isdigit()) >= 2
        has_symbol = sum(1 for c in password if c in string.punctuation) >= 2
        
        return has_upper and has_lower and has_digit and has_symbol


def main() -> None:
    """Command-line interface entrypoint."""
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure passwords."
    )
    
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=16,
        help="Password length (minimum 8, default: 16)"
    )
    parser.add_argument(
        "-a", "--all-symbols",
        action="store_true",
        help="Include all punctuation symbols without exclusion"
    )
    parser.add_argument(
        "-n", "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1)"
    )
    parser.add_argument(
        "-v", "--validate",
        type=str,
        help="Check if a specific password meets strength requirements"
    )
    
    args = parser.parse_args()
    
    # Handle direct strength validation if requested
    if args.validate:
        is_valid = PasswordGenerator.is_strong(args.validate)
        if is_valid:
            print(f"[+] '{args.validate}' meets strength requirements.")
        else:
            print(f"[-] '{args.validate}' fails strength requirements.")
        return
    
    # Generate requested passwords
    try:
        generator = PasswordGenerator(
            default_length=args.length,
            include_all_symbols=args.all_symbols
        )
        for _ in range(args.count):
            print(generator.generate())
    except ValueError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()