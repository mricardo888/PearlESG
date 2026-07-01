from cryptography.fernet import Fernet
from typing import Union

def encrypt_data(data: Union[str, bytes], key: bytes) -> bytes:
    """Encrypt data using AES-256."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    """Decrypt data and return as string."""
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_data)
    return decrypted.decode('utf-8')