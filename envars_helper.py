# envars_helper.py
import base64
import os
from typing import Optional
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


class EncryptionHelper:
    """ابزار رمزنگاری و رمزگشایی امن فایل‌ها با استفاده از Scrypt و Fernet."""

    @classmethod
    def generate_key(
        cls, password: str, filename: str, save_salt: bool = True
    ) -> bytes:
        """تولید کلید رمزنگاری از طریق مشتق‌سازی پسورد با Scrypt."""
        salt_file = f"{filename}.salt"

        if os.path.exists(salt_file):
            with open(salt_file, "rb") as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            if save_salt:
                with open(salt_file, "wb") as f:
                    f.write(salt)

        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @classmethod
    def encrypt(
        cls, filename: str, key: bytes, remove_original: bool = False
    ) -> Optional[str]:
        """رمزنگاری فایل ورودی و ساخت فایل خروجی با پسوند .envs."""
        try:
            if not os.path.exists(filename):
                print(f"Error: Target file '{filename}' does not exist.")
                return None

            fernet = Fernet(key)
            with open(filename, "rb") as f:
                file_data = f.read()

            encrypted_data = fernet.encrypt(file_data)

            with open(f"{filename}.envs", "wb") as f:
                f.write(encrypted_data)

            if remove_original:
                os.remove(filename)

            return "File encrypted successfully..."
        except Exception as e:
            print(f"Encryption error: {e}")
            return None

    @classmethod
    def decrypt(cls, filename: str, key: bytes) -> Optional[str]:
        """رمزگشایی فایل .envs و بازگردانی فایل اصلی."""
        try:
            if not os.path.exists(filename):
                print(f"Error: Encrypted file '{filename}' does not exist.")
                return None

            fernet = Fernet(key)
            with open(filename, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            original_filename = (
                filename[:-5] if filename.endswith(".envs") else f"decrypted_{filename}"
            )

            with open(original_filename, "wb") as f:
                f.write(decrypted_data)

            return "File decrypted successfully..."

        except InvalidToken:
            print("Decryption failed: invalid key or corrupted data")
            return None
        except Exception as e:
            print(f"Decryption error: {e}")
            return None
