from app.vault import (
    create_entry,
    deserialize_entries,
    entry_already_exists,
    is_valid_entry,
    load_entries,
    save_entries,
    search_entries,
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


def test_valid_entry_requires_website_username_and_password():
    assert is_valid_entry(
        "example.com",
        "alice@example.com",
        "secret-password",
    )

    assert not is_valid_entry("", "alice@example.com", "secret-password")
    assert not is_valid_entry("example.com", "", "secret-password")
    assert not is_valid_entry("example.com", "alice@example.com", "")


def test_entry_already_exists_uses_website_and_username():
    entries = [
        create_entry(
            "example.com",
            "alice@example.com",
            "secret-password",
        )
    ]

    assert entry_already_exists(
        entries,
        "EXAMPLE.COM",
        "alice@example.com",
    )

    assert not entry_already_exists(
        entries,
        "example.com",
        "another@example.com",
    )


def test_search_entries_finds_website_or_username():
    entries = [
        create_entry("example.com", "alice@example.com", "password-1"),
        create_entry("github.com", "bob@github.com", "password-2"),
    ]

    assert search_entries(entries, "EXAMPLE") == [entries[0]]
    assert search_entries(entries, "bob") == [entries[1]]
    assert search_entries(entries, "missing") == []
    assert search_entries(entries, "") == []
    