import getpass
import keyring
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os
import base64

SERVICE_NAME = "Scope3CarbonCalculator"

def get_or_set_master_key():
    # Retrieve or prompt for master password
    password = keyring.get_password(SERVICE_NAME, "master")
    if not password:
        password = getpass.getpass("Enter master password: ")
        keyring.set_password(SERVICE_NAME, "master", password)
    # Derive AES key
    salt = b'static_salt_change_in_production'  # Use os.urandom(16) in production
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                     iterations=600000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key