# test_envars_helper.py
import os
import unittest
from envars_helper import EncryptionHelper


class TestEncryptionHelper(unittest.TestCase):

    def setUp(self):
        self.password = "*******"
        self.filename = "sample_test.env"
        self.encrypted_filename = f"{self.filename}.envs"
        self.salt_filename = f"{self.filename}.salt"
        self.sample_content = b"DATABASE_URL=*******"

        with open(self.filename, "wb") as f:
            f.write(self.sample_content)

    def tearDown(self):
        for filepath in [self.filename, self.encrypted_filename, self.salt_filename]:
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_generate_key(self):
        key = EncryptionHelper.generate_key(self.password, self.filename, save_salt=True)
        self.assertIsInstance(key, bytes)
        self.assertTrue(os.path.exists(self.salt_filename))

    def test_encrypt(self):
        key = EncryptionHelper.generate_key(self.password, self.filename)
        result = EncryptionHelper.encrypt(self.filename, key)
        self.assertEqual(result, "File encrypted successfully...")
        self.assertTrue(os.path.exists(self.encrypted_filename))

    def test_full_encryption_decryption_flow(self):
        key = EncryptionHelper.generate_key(self.password, self.filename)
        EncryptionHelper.encrypt(self.filename, key)
        os.remove(self.filename)

        result = EncryptionHelper.decrypt(self.encrypted_filename, key)
        self.assertEqual(result, "File decrypted successfully...")
        self.assertTrue(os.path.exists(self.filename))

        with open(self.filename, "rb") as f:
            restored_content = f.read()
        self.assertEqual(restored_content, self.sample_content)

    def test_decrypt_nonexistent_file(self):
        key = EncryptionHelper.generate_key(self.password, self.filename)
        result = EncryptionHelper.decrypt("missing_file.envs", key)
        self.assertIsNone(result)

    def test_decrypt_with_wrong_key(self):
        key = EncryptionHelper.generate_key(self.password, self.filename)
        EncryptionHelper.encrypt(self.filename, key)
        wrong_key = EncryptionHelper.generate_key("wrong_password", self.filename)
        result = EncryptionHelper.decrypt(self.encrypted_filename, wrong_key)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
