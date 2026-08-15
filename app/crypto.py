import os

from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit encryption key from the master password.
    """

    return hash_secret_raw(
        secret=master_password.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        type=Type.ID,
    )


def generate_salt() -> bytes:
    """
    Generate a cryptographically secure random salt.
    """

    return os.urandom(16)


def encrypt_data(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    """
    Encrypt data using AES-256-GCM.

    Returns:
        encrypted_data, nonce
    """

    nonce = os.urandom(12)
    aesgcm = AESGCM(key)

    encrypted_data = aesgcm.encrypt(
        nonce,
        data,
        None
    )

    return encrypted_data, nonce


def decrypt_data(
    encrypted_data: bytes,
    key: bytes,
    nonce: bytes
) -> bytes:
    """
    Decrypt data using AES-256-GCM.
    """

    aesgcm = AESGCM(key)

    return aesgcm.decrypt(
        nonce,
        encrypted_data,
        None
    )