from cryptography.fernet import Fernet

def encrypt_data(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(encrypted_data)