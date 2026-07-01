import getpass
import keyring
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

SERVICE_NAME = "HKEX_Scope3_Carbon_Calculator"

def get_or_create_master_key() -> bytes:
    """Retrieve or prompt for master password and derive AES-256 key."""
    password = keyring.get_password(SERVICE_NAME, "master")
    if not password:
        password = getpass.getpass("Enter master password for data protection: ")
        confirm = getpass.getpass("Confirm master password: ")
        if password != confirm:
            raise ValueError("Passwords do not match.")
        keyring.set_password(SERVICE_NAME, "master", password)
    
    # Salt should be stored securely or derived consistently; use random in production
    salt = b'HKEX_Scope3_Salt_2026'  # Change and manage securely in production
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=600000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def clear_master_password():
    """Optional: Clear stored password (for logout/reset)."""
    keyring.delete_password(SERVICE_NAME, "master")