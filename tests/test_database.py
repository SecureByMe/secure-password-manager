import sqlite3

from app.database import create_database, DATABASE_NAME
from app.database import load_vault, save_vault



def test_database_creation(tmp_path, monkeypatch):
    database_path = tmp_path / "test_vault.db"

    monkeypatch.setattr(
        "app.database.DATABASE_NAME",
        str(database_path)
    )

    create_database()

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name='vault'
        """
    )

    result = cursor.fetchone()

    connection.close()

    assert result is not None
def test_vault_data_is_encrypted_and_can_be_loaded(tmp_path, monkeypatch):
    database_path = tmp_path / "test_vault.db"

    monkeypatch.setattr(
        "app.database.DATABASE_NAME",
        str(database_path),
    )

    master_password = "my-strong-master-password"
    vault_data = b'{"website": "example.com", "password": "secret123"}'

    save_vault(master_password, vault_data)

    loaded_data = load_vault(master_password)

    assert loaded_data == vault_data

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT encrypted_data FROM vault WHERE id = 1"
    )

    encrypted_data = cursor.fetchone()[0]
    connection.close()

    assert encrypted_data != vault_data
    