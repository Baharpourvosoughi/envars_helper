# Secure File Vault (EncryptionHelper)

A professional-grade file encryption tool built in Python. This project demonstrates the implementation of secure cryptographic standards, specifically designed to protect sensitive files using modern key derivation and symmetric encryption.

## Features
- **Secure Key Derivation:** Uses `Scrypt` (a memory-hard KDF) to transform user passwords into robust cryptographic keys.
- **Symmetric Encryption:** Utilizes `Fernet` (AES-128-CBC + HMAC) to ensure data confidentiality and integrity.
- **Salt Management:** Automatically manages unique salt files for every password-derived key, preventing rainbow table attacks.
- **Clean API:** A modular, class-based architecture that is easy to integrate into larger applications.

## Technical Stack
- **Language:** Python 3.x
- **Libraries:** 
    - `cryptography`: For high-level cryptographic recipes.
    - `os` & `base64`: For system interaction and data encoding.

## How it works
This tool follows a professional pipeline:
1. **Key Generation:** A password and a unique salt are processed via `Scrypt` to produce a 32-byte key.
2. **Encryption:** The generated key powers the `Fernet` engine to lock your files.
3. **Decryption:** The same password (along with the original salt file) regenerates the exact key required to unlock the data.

## Security Disclaimer
This tool is built for educational purposes and personal file security. When using it in production, ensure that:
1. **Your *.salt files are stored securely alongside the encrypted files.
2. **You use strong, unique passwords for key derivation.
