"""
CipherForge - Comprehensive Encryption Engine
Supports AES-GCM, AES-CBC, ChaCha20 with RSA-2048 digital signatures.
"""

import os
import base64
import json
from datetime import datetime

from Crypto.Cipher import AES, ChaCha20
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class CryptoEngine:
    ALGORITHMS = ["AES-GCM", "AES-CBC", "ChaCha20"]

    def __init__(self, key_dir=None):
        self.key_dir = key_dir or os.path.join(os.path.expanduser("~"), ".cipherforge")
        os.makedirs(self.key_dir, exist_ok=True)
        self.private_key_path = os.path.join(self.key_dir, "private_key.pem")
        self.public_key_path = os.path.join(self.key_dir, "public_key.pem")
        self.enc_key_path = os.path.join(self.key_dir, "encryption_key.key")
        self.history = []
        self._ensure_rsa_keys()

    def _ensure_rsa_keys(self):
        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            key = RSA.generate(2048)
            with open(self.private_key_path, "wb") as f:
                f.write(key.export_key())
            with open(self.public_key_path, "wb") as f:
                f.write(key.publickey().export_key())

    def get_public_key(self) -> str:
        with open(self.public_key_path, "r") as f:
            return f.read()

    def _get_cipher(self, algorithm: str, key: bytes):
        if algorithm == "AES-GCM":
            nonce = get_random_bytes(12)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            return cipher, nonce
        elif algorithm == "AES-CBC":
            iv = get_random_bytes(AES.block_size)
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            return cipher, iv
        elif algorithm == "ChaCha20":
            cipher = ChaCha20.new(key=key)
            return cipher, cipher.nonce
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

    def _sign_data(self, data: bytes) -> bytes:
        with open(self.private_key_path, "r") as f:
            key = RSA.import_key(f.read())
        h = SHA256.new(data)
        return pkcs1_15.new(key).sign(h)

    def _verify_sig(self, data: bytes, signature: bytes) -> bool:
        with open(self.public_key_path, "r") as f:
            key = RSA.import_key(f.read())
        h = SHA256.new(data)
        try:
            pkcs1_15.new(key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def _log(self, action: str, algorithm: str, input_type: str, status: str, details: str = ""):
        self.history.insert(0, {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action": action,
            "algorithm": algorithm,
            "input_type": input_type,
            "status": status,
            "details": details,
        })
        if len(self.history) > 100:
            self.history = self.history[:100]

    def encrypt_text(self, algorithm: str, plaintext: str) -> str:
        if not plaintext.strip():
            raise ValueError("Input text is empty")

        key = get_random_bytes(32)
        cipher, nonce_or_iv = self._get_cipher(algorithm, key)
        data = plaintext.encode("utf-8")

        if algorithm == "AES-CBC":
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        else:
            encrypted_data = cipher.encrypt(data)

        signature = self._sign_data(encrypted_data)

        output = {
            "algorithm": algorithm,
            "nonce_or_iv": base64.b64encode(nonce_or_iv).decode("utf-8"),
            "ciphertext": base64.b64encode(encrypted_data).decode("utf-8"),
            "signature": base64.b64encode(signature).decode("utf-8"),
        }

        output_str = base64.b64encode(json.dumps(output).encode("utf-8")).decode("utf-8")

        with open(self.enc_key_path, "wb") as f:
            f.write(key)

        self._log("encrypt", algorithm, "text", "success", f"Encrypted {len(data)} bytes")
        return output_str

    def decrypt_text(self, ciphertext_b64: str) -> str:
        if not os.path.exists(self.enc_key_path):
            raise ValueError("No encryption key found. Encrypt something first.")

        with open(self.enc_key_path, "rb") as f:
            key = f.read()

        encrypted_data = json.loads(base64.b64decode(ciphertext_b64).decode("utf-8"))
        algorithm = encrypted_data["algorithm"]
        nonce_or_iv = base64.b64decode(encrypted_data["nonce_or_iv"])
        ct = base64.b64decode(encrypted_data["ciphertext"])
        sig = base64.b64decode(encrypted_data["signature"])

        if not self._verify_sig(ct, sig):
            self._log("decrypt", algorithm, "text", "failed", "Signature verification failed")
            raise ValueError("Digital signature verification failed!")

        if algorithm == "AES-GCM":
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce_or_iv)
            decrypted = cipher.decrypt(ct)
        elif algorithm == "AES-CBC":
            cipher = AES.new(key, AES.MODE_CBC, iv=nonce_or_iv)
            decrypted = unpad(cipher.decrypt(ct), AES.block_size)
        elif algorithm == "ChaCha20":
            cipher = ChaCha20.new(key=key, nonce=nonce_or_iv)
            decrypted = cipher.decrypt(ct)
        else:
            raise ValueError("Unsupported algorithm")

        self._log("decrypt", algorithm, "text", "success", f"Decrypted {len(ct)} bytes")
        return decrypted.decode("utf-8")

    def encrypt_file(self, algorithm: str, filepath: str) -> str:
        with open(filepath, "rb") as f:
            data = f.read()

        if not data:
            raise ValueError("File is empty")

        key = get_random_bytes(32)
        cipher, nonce_or_iv = self._get_cipher(algorithm, key)

        if algorithm == "AES-CBC":
            encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        else:
            encrypted_data = cipher.encrypt(data)

        signature = self._sign_data(encrypted_data)

        output = {
            "algorithm": algorithm,
            "nonce_or_iv": base64.b64encode(nonce_or_iv).decode("utf-8"),
            "ciphertext": base64.b64encode(encrypted_data).decode("utf-8"),
            "signature": base64.b64encode(signature).decode("utf-8"),
            "original_filename": os.path.basename(filepath),
        }

        output_str = base64.b64encode(json.dumps(output).encode("utf-8")).decode("utf-8")

        with open(self.enc_key_path, "wb") as f:
            f.write(key)

        # Save encrypted file
        out_path = os.path.splitext(filepath)[0] + ".enc"
        with open(out_path, "w") as f:
            f.write(output_str)

        self._log("encrypt", algorithm, "file", "success",
                  f"{os.path.basename(filepath)} ({len(data)} bytes)")
        return out_path

    def decrypt_file(self, enc_filepath: str) -> str:
        if not os.path.exists(self.enc_key_path):
            raise ValueError("No encryption key found. Encrypt something first.")

        with open(self.enc_key_path, "rb") as f:
            key = f.read()

        with open(enc_filepath, "r") as f:
            encrypted_data = json.loads(base64.b64decode(f.read()).decode("utf-8"))

        algorithm = encrypted_data["algorithm"]
        nonce_or_iv = base64.b64decode(encrypted_data["nonce_or_iv"])
        ct = base64.b64decode(encrypted_data["ciphertext"])
        sig = base64.b64decode(encrypted_data["signature"])
        original_name = encrypted_data.get("original_filename", "decrypted_file")

        if not self._verify_sig(ct, sig):
            self._log("decrypt", algorithm, "file", "failed", "Signature verification failed")
            raise ValueError("Digital signature verification failed!")

        if algorithm == "AES-GCM":
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce_or_iv)
            decrypted = cipher.decrypt(ct)
        elif algorithm == "AES-CBC":
            cipher = AES.new(key, AES.MODE_CBC, iv=nonce_or_iv)
            decrypted = unpad(cipher.decrypt(ct), AES.block_size)
        elif algorithm == "ChaCha20":
            cipher = ChaCha20.new(key=key, nonce=nonce_or_iv)
            decrypted = cipher.decrypt(ct)
        else:
            raise ValueError("Unsupported algorithm")

        out_dir = os.path.dirname(enc_filepath)
        out_path = os.path.join(out_dir, original_name)
        if os.path.exists(out_path):
            base, ext = os.path.splitext(out_path)
            out_path = f"{base}_decrypted{ext}"

        with open(out_path, "wb") as f:
            f.write(decrypted)

        self._log("decrypt", algorithm, "file", "success", f"{original_name}")
        return out_path

    def verify_signature_text(self, ciphertext_b64: str) -> dict:
        try:
            data = json.loads(base64.b64decode(ciphertext_b64.strip()).decode("utf-8"))
            ct = base64.b64decode(data["ciphertext"])
            sig = base64.b64decode(data["signature"])
            is_valid = self._verify_sig(ct, sig)
            algo = data.get("algorithm", "unknown")
            status = "success" if is_valid else "failed"
            self._log("verify", algo, "text", status,
                      "Valid" if is_valid else "Invalid")
            return {"valid": is_valid, "algorithm": algo}
        except Exception as e:
            self._log("verify", "unknown", "text", "error", str(e))
            return {"valid": False, "algorithm": "unknown", "error": str(e)}

    def verify_signature_file(self, filepath: str) -> dict:
        try:
            with open(filepath, "r") as f:
                content = f.read()
            return self.verify_signature_text(content)
        except Exception as e:
            self._log("verify", "unknown", "file", "error", str(e))
            return {"valid": False, "algorithm": "unknown", "error": str(e)}

    def has_encryption_key(self) -> bool:
        return os.path.exists(self.enc_key_path)

    def get_history(self) -> list:
        return self.history
