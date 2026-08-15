import json


def create_entry(
    website: str,
    username: str,
    password: str,
    notes: str = "",
) -> dict[str, str]:
    """Create one password-vault entry."""

    return {
        "website": website,
        "username": username,
        "password": password,
        "notes": notes,
    }


def serialize_entries(entries: list[dict[str, str]]) -> bytes:
    """Convert vault entries into bytes ready for encryption."""

    return json.dumps(entries).encode("utf-8")


def deserialize_entries(data: bytes) -> list[dict[str, str]]:
    """Convert decrypted vault bytes back into entries."""

    return json.loads(data.decode("utf-8"))
