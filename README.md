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
python string_manipulator.py encrypt "Hello World" --seed 40
```

Decrypt:

```bash
python string_manipulator.py decrypt "{HGGYWMYsG;" --seed 40
```

Available shuffle modes are `fisher_yates`, `sample`, and `deterministic`.

## Testing

The project uses Python's built-in `unittest` framework. No additional testing packages are required.

The test suite is located in the `tests/` directory:

```text
tests/
├── __init__.py
├── test_cipher_table.py
├── test_password_generator.py
└── test_string_manipulator.py
```

### Run All Tests

From the project root directory, run:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

This automatically discovers and runs all test files in the `tests/` directory.

### Run a Specific Test File

To run only the cipher table tests:

```bash
python -m unittest tests.test_cipher_table -v
```

To run only the password generator tests:

```bash
python -m unittest tests.test_password_generator -v
```

To run only the string manipulator tests:

```bash
python -m unittest tests.test_string_manipulator -v
```

### Test Output

A successful test run will display the individual tests and finish with a summary similar to:

```text
Ran XX tests in X.XXXs

OK
```

If a test fails, `unittest` will display the failing test and the associated error or assertion message.

## Security Note

The password generator uses cryptographically secure randomness. The custom cipher and substitution tools are primarily intended for **learning and experimentation** and should not be used as replacements for modern, established encryption standards.

## License

This project is provided for educational and general-purpose use.
