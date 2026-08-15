from getpass import getpass

from cryptography.exceptions import InvalidTag
from app.generator import generate_password

from app.vault import (
    create_entry,
    entry_already_exists,
    is_valid_entry,
    load_entries,
    save_entries,
)


def show_entries(entries: list[dict[str, str]]) -> None:
    """List saved entries without displaying passwords."""

    if not entries:
        print("\nYour vault is empty.\n")
        return

    print("\n--- Vault Entries ---")

    for number, entry in enumerate(entries, start=1):
        print(f"\n{number}. Website: {entry['website']}")
        print(f"   Username: {entry['username']}")
        print(f"   Notes: {entry['notes']}")
def get_password_for_new_entry() -> str:
    """Ask whether to generate a password or enter one manually."""

    choice = input("Generate a secure password? (y/n): ").strip().lower()

    if choice != "y":
        return getpass("Password to save: ")

    length_text = input("Password length [16]: ").strip()

    try:
        length = int(length_text) if length_text else 16
        password = generate_password(length)
    except ValueError:
        print("\nInvalid length. Using 16 characters.")
        password = generate_password()

    print(f"\nGenerated password: {password}")

    return password
        


def add_entry(
    entries: list[dict[str, str]],
    master_password: str,
) -> None:
    """Add a new validated password entry."""

    website = input("Website: ").strip()
    username = input("Username: ").strip()
    password = get_password_for_new_entry()
    notes = input("Notes (optional): ").strip()

    if not is_valid_entry(website, username, password):
        print("\nWebsite, username, and password are required.")
        return

    if entry_already_exists(entries, website, username):
        print("\nAn entry for this website and username already exists.")
        return

    entries.append(create_entry(
        website,
        username,
        password,
        notes,
    ))

    save_entries(master_password, entries)

    print("\nEntry encrypted and saved.")


def reveal_password(entries: list[dict[str, str]]) -> None:
    """Reveal the password for one selected entry."""

    if not entries:
        print("\nYour vault is empty.\n")
        return

    show_entries(entries)
    choice = input("\nEntry number to reveal: ")

    try:
        entry = entries[int(choice) - 1]
    except (ValueError, IndexError):
        print("\nInvalid entry number.")
        return

    print(f"\nPassword for {entry['website']}: {entry['password']}")


def edit_entry(
    entries: list[dict[str, str]],
    master_password: str,
) -> None:
    """Edit one selected vault entry."""

    if not entries:
        print("\nYour vault is empty.\n")
        return

    show_entries(entries)
    choice = input("\nEntry number to edit: ")

    try:
        entry = entries[int(choice) - 1]
    except (ValueError, IndexError):
        print("\nInvalid entry number.")
        return

    website = input(f"Website [{entry['website']}]: ").strip()
    username = input(f"Username [{entry['username']}]: ").strip()
    password = getpass("New password (leave blank to keep current): ")
    notes = input(f"Notes [{entry['notes']}]: ").strip()

    if website:
        entry["website"] = website

    if username:
        entry["username"] = username

    if password:
        entry["password"] = password

    if notes:
        entry["notes"] = notes

    save_entries(master_password, entries)

    print("\nEntry updated and encrypted.")


def change_master_password(
    entries: list[dict[str, str]],
    current_master_password: str,
) -> str:
    """Re-encrypt the vault using a new master password."""

    new_master_password = getpass("New master password: ")
    confirm_password = getpass("Confirm new master password: ")

    if not new_master_password:
        print("\nMaster password cannot be empty.")
        return current_master_password

    if new_master_password != confirm_password:
        print("\nPasswords do not match. Nothing was changed.")
        return current_master_password

    save_entries(new_master_password, entries)

    print("\nMaster password changed. Vault re-encrypted.")

    return new_master_password


def delete_entry(
    entries: list[dict[str, str]],
    master_password: str,
) -> None:
    """Delete one selected vault entry after confirmation."""

    if not entries:
        print("\nYour vault is empty.\n")
        return

    show_entries(entries)
    choice = input("\nEntry number to delete: ")

    try:
        entry_number = int(choice)
        entry = entries[entry_number - 1]
    except (ValueError, IndexError):
        print("\nInvalid entry number.")
        return

    confirmation = input(
        f"Type DELETE to remove {entry['website']}: "
    )

    if confirmation != "DELETE":
        print("\nDeletion cancelled.")
        return

    entries.pop(entry_number - 1)
    save_entries(master_password, entries)

    print("\nEntry deleted.")


def main() -> None:
    """Run the SecureVault command-line menu."""

    print("Welcome to SecureVault")

    master_password = getpass("Master password: ")

    try:
        entries = load_entries(master_password)
    except InvalidTag:
        print("\nIncorrect master password or damaged vault.")
        return

    while True:
        print("\n1. Add password entry")
        print("2. List password entries")
        print("3. Reveal a password")
        print("4. Edit an entry")
        print("5. Delete an entry")
        print("6. Change master password")
        print("7. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_entry(entries, master_password)

        elif choice == "2":
            show_entries(entries)

        elif choice == "3":
            reveal_password(entries)

        elif choice == "4":
            edit_entry(entries, master_password)

        elif choice == "5":
            delete_entry(entries, master_password)

        elif choice == "6":
            master_password = change_master_password(
                entries,
                master_password,
            )

        elif choice == "7":
            print("\nVault closed.")
            break

        else:
            print("\nPlease choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
