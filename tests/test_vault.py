from app.vault import create_entry, deserialize_entries, serialize_entries


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
    