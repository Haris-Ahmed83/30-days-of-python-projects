# Day 3: Password Manager

## Description
An encrypted local password manager built with Python. It uses the `cryptography` library to implement AES encryption via the Fernet recipe. Users can store and retrieve passwords using a master password that derives a secure encryption key.

## Features
- **Master Password Protection**: Uses PBKDF2HMAC for secure key derivation.
- **AES Encryption**: Passwords are encrypted using Fernet (AES-128 in CBC mode with HMAC-SHA256).
- **Local Storage**: Data is stored in a local `passwords.json` file.
- **CLI Interface**: Simple and intuitive command-line interface.

## Requirements
- Python 3.x
- `cryptography` library

## How to Run
1. Install dependencies:
   ```bash
   pip install cryptography
   ```
2. Run the script:
   ```bash
   python password_manager.py
   ```
3. Follow the on-screen prompts to add or retrieve passwords.
