# Personal Password Manager

## About

A command-line application that securely stores passwords
using encryption and master password authentication.

## Features

- Add website credentials
- Encrypt stored passwords
- View saved accounts
- Search accounts
- Update and delete credentials
- Generate strong passwords
- Master password authentication

## Technologies Used

- Python
- JSON
- Cryptography
- File Handling
- Modules
- Random Password Generation

## Installation

Install the dependency:

pip install -r requirements.txt

## How to Run

python main.py

## Security

Passwords are encrypted using Fernet.
The encryption key is derived from the master password
using PBKDF2-HMAC-SHA256.

Never upload personal password data to GitHub.

## Author

Python Projects Challenge
