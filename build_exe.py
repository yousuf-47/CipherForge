#!/usr/bin/env python3
"""
CipherForge - Build Script
Builds the desktop application into a standalone executable using PyInstaller.

Usage:
    python build_exe.py

This creates a dist/CipherForge/ directory with the executable.
"""

import os
import sys
import subprocess
import platform


def build():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Determine platform-specific settings
    system = platform.system()
    separator = ";" if system == "Windows" else ":"

    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=CipherForge",
        "--windowed",           # No console window
        "--onedir",             # Create a directory bundle
        "--clean",              # Clean before building
        f"--distpath={os.path.join(base_dir, 'dist')}",
        f"--workpath={os.path.join(base_dir, 'build')}",
        f"--specpath={base_dir}",

        # Add all source files as data
        f"--add-data=theme.py{separator}.",
        f"--add-data=crypto_engine.py{separator}.",
        f"--add-data=panels{separator}panels",

        # Hidden imports needed
        "--hidden-import=customtkinter",
        "--hidden-import=pycryptodome",
        "--hidden-import=Crypto",
        "--hidden-import=Crypto.Cipher",
        "--hidden-import=Crypto.Cipher.AES",
        "--hidden-import=Crypto.Cipher.ChaCha20",
        "--hidden-import=Crypto.PublicKey",
        "--hidden-import=Crypto.PublicKey.RSA",
        "--hidden-import=Crypto.Signature",
        "--hidden-import=Crypto.Signature.pkcs1_15",
        "--hidden-import=Crypto.Hash",
        "--hidden-import=Crypto.Hash.SHA256",
        "--hidden-import=Crypto.Random",
        "--hidden-import=Crypto.Util.Padding",

        # Collect all of customtkinter
        "--collect-all=customtkinter",

        # Entry point
        os.path.join(base_dir, "main.py"),
    ]

    # Platform-specific icon
    icon_path = os.path.join(base_dir, "icon.ico")
    if os.path.exists(icon_path):
        cmd.insert(-1, f"--icon={icon_path}")

    print(f"\n{'='*60}")
    print(f"  CipherForge Build Script")
    print(f"  Platform: {system} ({platform.machine()})")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"{'='*60}\n")

    print("Building CipherForge executable...\n")

    result = subprocess.run(cmd, cwd=base_dir)

    if result.returncode == 0:
        dist_dir = os.path.join(base_dir, "dist", "CipherForge")
        print(f"\n{'='*60}")
        print(f"  BUILD SUCCESSFUL!")
        print(f"  Output: {dist_dir}")
        if system == "Windows":
            print(f"  Run: dist\\CipherForge\\CipherForge.exe")
        elif system == "Darwin":
            print(f"  Run: dist/CipherForge/CipherForge")
        else:
            print(f"  Run: dist/CipherForge/CipherForge")
        print(f"{'='*60}\n")
    else:
        print(f"\n  BUILD FAILED (exit code {result.returncode})")
        sys.exit(1)


if __name__ == "__main__":
    build()
