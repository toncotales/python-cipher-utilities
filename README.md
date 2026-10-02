# Python Cipher Utilities

A collection of simple Python utilities for **encryption, decryption, password generation, and string manipulation**.

## Features

* **Vigenère-style cipher** — Encrypt and decrypt text using a repeating keyword.
* **Password generator** — Generate cryptographically secure passwords and check password strength.
* **String manipulator** — Shuffle, unshuffle, and perform seed-based substitution encryption/decryption.

## Files

| File                    | Description                               |
| ----------------------- | ----------------------------------------- |
| `cipher_table.py`       | Vigenère-style encryption and decryption  |
| `password_generator.py` | Secure password generation and validation |
| `string_manipulator.py` | String shuffling and substitution cipher  |

## Requirements

* Python 3.10+
* No external dependencies

## Usage

### Cipher Table

Encrypt:

```bash
python cipher_table.py encrypt "Hello World" -k SECRET
```

Decrypt:

```bash
python cipher_table.py decrypt ":IN2SS}ST2H" -k SECRET
```

A custom character set can also be provided with `--chars`.

### Password Generator

Generate a password:

```bash
python password_generator.py
```

Generate a 20-character password:

```bash
python password_generator.py --length 20
```

Generate multiple passwords:

```bash
python password_generator.py --length 20 --count 5
```

Validate a password:

```bash
python password_generator.py --validate "MyPassword123!!"
```

The generator requires a minimum length of 8 characters and uses Python's `secrets` module for secure random generation.

### String Manipulator

Shuffle a string:

```bash
python string_manipulator.py shuffle "Hello World"
```

Choose a shuffle mode:

```bash
python string_manipulator.py shuffle "Hello World" --mode deterministic
```

Unshuffle:

```bash
python string_manipulator.py unshuffle "ollr WloHed"
```

Encrypt:

```bash
python string_manipulator.py encrypt "Hello World" --seed 42
```

Decrypt:

```bash
python string_manipulator.py decrypt "..." --seed 42
```

Available shuffle modes are `fisher_yates`, `sample`, and `deterministic`.

## Security Note

The password generator uses cryptographically secure randomness. The custom cipher and substitution tools are primarily intended for **learning and experimentation** and should not be used as replacements for modern, established encryption standards.

## License

This project is provided for educational and general-purpose use.
