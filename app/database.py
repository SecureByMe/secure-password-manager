import sqlite3

from app.crypto import decrypt_data, derive_key, encrypt_data, generate_salt


DATABASE_NAME = "vault.db"


def create_database() -> None:
    """Create the local encrypted vault database."""

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY,
            salt BLOB NOT NULL,
            nonce BLOB NOT NULL,
            encrypted_data BLOB NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_vault(master_password: str, data: bytes) -> None:
    """Encrypt and save vault data."""

    create_database()

    salt = generate_salt()
    key = derive_key(master_password, salt)
    encrypted_data, nonce = encrypt_data(data, key)

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO vault (id, salt, nonce, encrypted_data)
        VALUES (1, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            salt = excluded.salt,
            nonce = excluded.nonce,
            encrypted_data = excluded.encrypted_data
        """,
        (salt, nonce, encrypted_data),
    )

    connection.commit()
    connection.close()


def load_vault(master_password: str) -> bytes | None:
    """Load and decrypt vault data."""

    create_database()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT salt, nonce, encrypted_data
        FROM vault
        WHERE id = 1
        """
    )

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    salt, nonce, encrypted_data = result
    key = derive_key(master_password, salt)

    return decrypt_data(encrypted_data, key, nonce)