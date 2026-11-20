import os
import base64
import hashlib

from cryptography.fernet import Fernet


def derive_key(master_password, salt):
    key = hashlib.pbkdf2_hmac(
        "sha256",
        master_password.encode("utf-8"),
        salt,
        600000,
        dklen=32
    )

    return base64.urlsafe_b64encode(key)


def create_master(master_password):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)

    verifier = Fernet(key).encrypt(
        b"password-manager-verification"
    ).decode("utf-8")

    return {
        "salt": base64.b64encode(salt).decode("utf-8"),
        "verifier": verifier
    }


def verify_master(master_password, master_data):
    salt = base64.b64decode(master_data["salt"])
    key = derive_key(master_password, salt)

    try:
        decrypted = Fernet(key).decrypt(
            master_data["verifier"].encode("utf-8")
        )

        return decrypted == b"password-manager-verification"

    except Exception:
        return False


def encrypt_password(password, master_password, salt):
    key = derive_key(master_password, salt)
    return Fernet(key).encrypt(
        password.encode("utf-8")
    ).decode("utf-8")


def decrypt_password(encrypted_password, master_password, salt):
    key = derive_key(master_password, salt)

    return Fernet(key).decrypt(
        encrypted_password.encode("utf-8")
    ).decode("utf-8")
