from app.vault import create_entry, deserialize_entries, serialize_entries
from app.vault import (
    create_entry,
    deserialize_entries,
    load_entries,
    save_entries,
    serialize_entries,
)


def test_create_entry():
    entry = create_entry(
        "example.com",
        "alice@example.com",
        "secret-password",
        "Personal account",
    )

    assert entry["website"] == "example.com"
    assert entry["username"] == "alice@example.com"
    assert entry["password"] == "secret-password"
    assert entry["notes"] == "Personal account"


def test_entries_can_be_serialized_and_deserialized():
    entries = [
        create_entry(
            "example.com",
            "alice@example.com",
            "secret-password",
        )
    ]

    encrypted_ready_data = serialize_entries(entries)
    restored_entries = deserialize_entries(encrypted_ready_data)

    assert restored_entries == entries
def test_entries_can_be_saved_and_loaded(tmp_path, monkeypatch):
    database_path = tmp_path / "test_vault.db"

    monkeypatch.setattr(
        "app.database.DATABASE_NAME",
        str(database_path),
    )

    master_password = "my-master-password"

    entries = [
        create_entry(
            "example.com",
            "alice@example.com",
            "secret-password",
            "Personal account",
        )
    ]

    save_entries(master_password, entries)

    loaded_entries = load_entries(master_password)

    assert loaded_entries == entries
    