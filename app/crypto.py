from argon2.low_level import hash_secret_raw, Type
import os


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