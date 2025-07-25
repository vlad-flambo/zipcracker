
# zipcracker

## Description
`zipcracker` is a command-line tool for brute-force cracking password-protected ZIP files using customizable character sets and password lengths.

## Features
- Brute-force attack on ZIP file passwords
- Customizable password length and character set
- Uses efficient itertools for password generation
- Multiprocessing support for faster cracking
- Progress bar with tqdm (if installed)
- Handles errors and invalid files gracefully

## Requirements
- Python 3.6 or higher
- [pyzipper](https://pypi.org/project/pyzipper/) (`pip install pyzipper`)
- [tqdm](https://pypi.org/project/tqdm/) (optional, for progress bar)

## Usage

```sh
python zipcracker.py <zipfilename> <password_length> [--charset CHARSET]
```

- `<zipfilename>`: Path to the ZIP file to crack
- `<password_length>`: Length of the password to brute-force (integer)
- `--charset CHARSET`: (Optional) Characters to use for brute-force (default: all letters and digits)

### Example

```sh
python zipcracker.py secret.zip 4 --charset abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
```

## Notes on Multiprocessing (macOS)
- Always run the script as a standalone program (not from an interactive shell or notebook).
- Ensure all multiprocessing code is inside the `if __name__ == '__main__':` block (already handled in the script).

## Security Notice
This tool is for educational and authorized testing purposes only. Do not use it on files you do not own or have explicit permission to test.
