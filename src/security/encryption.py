from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class QKDEncryptor:
    def __init__(self, key):
        self.key = key
        self.backend = default_backend()

    def encrypt(self, plaintext):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.final()
        return iv + ciphertext

    def decrypt(self, ciphertext):
        iv = ciphertext[:16]
        cipher = Cipher(algorithms.AES(self.key), modes.CTR(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext[16:]) + decryptor.final()
