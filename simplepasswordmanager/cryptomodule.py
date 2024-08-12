from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
import string
import secrets
import hashlib


def derive_key(salt, password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_string(password, text):
    salt = os.urandom(16)
    key = derive_key(salt, password)

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(text.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return urlsafe_b64encode(salt + iv + ciphertext).decode()


def decrypt_string(password, encrypted_text):
    encrypted_data = urlsafe_b64decode(encrypted_text.encode())

    salt = encrypted_data[:16]
    iv = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    key = derive_key(salt, password)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    text = unpadder.update(padded_data) + unpadder.finalize()

    return text.decode()


def hash_password(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return sha256_hash


def decrypt_dict(password, data):
    return {
        key: decrypt_string(password, value)
        for key, value in data.items()
    }


def encrypt_dict(password, data):
    return {
        key: encrypt_string(password, value)
        for key, value in data.items()
    }


def generate_strong_password(length):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    while not (any(c.islower() for c in password) and
               any(c.isupper() for c in password) and
               any(c.isdigit() for c in password) and
               any(c in string.punctuation for c in password)):
        password = ''.join(secrets.choice(alphabet) for _ in range(length))

    return password


# print('GMAIL:', encrypt_string('123456', 'GMAIL'))
# print('password:', encrypt_string('123456', '123'))
# a = hash_password('123456')
# print(a)

