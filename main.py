from getpass import getpass

from cryptography.exceptions import InvalidTag

from app.vault import create_entry, load_entries, save_entries


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


def reveal_password(entries: list[dict[str, str]]) -> None:
    """Reveal the password for one selected entry."""

    if not entries:
        print("\nYour vault is empty.\n")
        return

    show_entries(entries)

    choice = input("\nEntry number to reveal: ")

    try:
        entry_number = int(choice)
        entry = entries[entry_number - 1]
    except (ValueError, IndexError):
        print("\nInvalid entry number.")
        return

    print(f"\nPassword for {entry['website']}: {entry['password']}")


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
        print("4. Exit")

        choice = input("\nChoose an option: ")

        if choice == "1":
            website = input("Website: ")
            username = input("Username: ")
            password = getpass("Password to save: ")
            notes = input("Notes (optional): ")

            entries.append(create_entry(
                website, username, password, notes
            ))
            save_entries(master_password, entries)

            print("\nEntry encrypted and saved.")

        elif choice == "2":
            show_entries(entries)

        elif choice == "3":
            reveal_password(entries)

        elif choice == "4":
            print("\nVault closed.")
            break

        else:
            print("\nPlease choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
    