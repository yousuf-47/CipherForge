# CipherForge - Comprehensive Encryption Tool

A cyberpunk-themed desktop application for military-grade encryption. Supports **AES-GCM**, **AES-CBC**, and **ChaCha20** algorithms with **RSA-2048** digital signature verification.

## Features

- **3 Encryption Algorithms**: AES-GCM (authenticated), AES-CBC (block cipher), ChaCha20 (stream cipher)
- **RSA Digital Signatures**: Auto-generated 2048-bit RSA keys for data signing & verification
- **Text & File Encryption**: Encrypt/decrypt both text input and files
- **Key Management**: View RSA public key, check encryption key status
- **Activity History**: Full log of all encryption/decryption operations
- **Cyberpunk UI**: Dark void theme with neon cyan/green/purple accents

## Quick Start

### Run Directly (Python)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python main.py
```

### Build Standalone Executable

```bash
# 1. Install dependencies (including PyInstaller)
pip install -r requirements.txt

# 2. Build the executable
python build_exe.py

# 3. Run the executable
# Windows: dist\CipherForge\CipherForge.exe
# macOS:   dist/CipherForge/CipherForge
# Linux:   dist/CipherForge/CipherForge
```

## Usage

### Encrypting Text
1. Click **INITIALIZE SESSION** on the landing screen
2. Select an encryption algorithm (AES-GCM, AES-CBC, or ChaCha20)
3. Choose **TEXT** input mode
4. Enter your plaintext in the input field
5. Click **ENCRYPT DATA**
6. Copy or save the encrypted output

### Encrypting Files
1. Select an algorithm
2. Choose **FILE** input mode
3. Click the drop zone to select a file
4. Click **ENCRYPT DATA**
5. The encrypted `.enc` file is saved next to the original

### Decrypting
1. Switch to the **DECRYPT** tab
2. Paste encrypted text or select an encrypted file
3. Click **DECRYPT DATA**
4. The original content is restored

### Verifying Signatures
1. Switch to the **VERIFY SIG** tab
2. Paste encrypted data or select an encrypted file
3. Click **VERIFY SIGNATURE**
4. A visual indicator shows if the signature is valid

## File Structure

```
desktop_app/
  main.py              # Application entry point & main window
  crypto_engine.py     # Encryption/decryption/signing engine
  theme.py             # Cyberpunk theme, colors, custom widgets
  panels/
    encrypt_panel.py   # Encryption interface
    decrypt_panel.py   # Decryption interface
    verify_panel.py    # Signature verification
    keys_panel.py      # Key management display
    history_panel.py   # Activity log
  requirements.txt     # Python dependencies
  build_exe.py         # PyInstaller build script
  README.md            # This file
```

## Key Storage

RSA keys and encryption keys are stored in: `~/.cipherforge/`
- `private_key.pem` - RSA private key (never share!)
- `public_key.pem` - RSA public key
- `encryption_key.key` - Symmetric encryption key for current session

## System Requirements

- Python 3.8+
- Works on Windows, macOS, and Linux
- No internet connection required (fully offline)

## Based On

Original project: [Comprehensive-Encryption-Tool](https://github.com/yousuf-47/Comprehensive-Encryption-Tool) by yousuf-47
