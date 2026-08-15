import json
from app.database import load_vault, save_vault


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

def save_entries(
    master_password: str,
    entries: list[dict[str, str]],
) -> None:
    """Serialize, encrypt, and save all vault entries."""

    data = serialize_entries(entries)
    save_vault(master_password, data)


def load_entries(master_password: str) -> list[dict[str, str]]:
    """Load, decrypt, and deserialize all vault entries."""

    data = load_vault(master_password)

    if data is None:
        return []

    return deserialize_entries(data)
