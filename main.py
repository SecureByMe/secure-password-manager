from getpass import getpass

from cryptography.exceptions import InvalidTag

from app.vault import create_entry, load_entries, save_entries


def show_entries(entries: list[dict[str, str]]) -> None:
    if not entries:
        print("\nYour vault is empty.\n")
        return

    print("\n--- Vault Entries ---")

    for number, entry in enumerate(entries, start=1):
        print(f"\n{number}. Website: {entry['website']}")
        print(f"   Username: {entry['username']}")
        print(f"   Password: {entry['password']}")
        print(f"   Notes: {entry['notes']}")


def main() -> None:
    print("Welcome to SecureVault")

    master_password = getpass("Master password: ")

    try:
        entries = load_entries(master_password)
    except InvalidTag:
        print("\nIncorrect master password or damaged vault.")
        return

    while True:
        print("\n1. Add password entry")
        print("2. View password entries")
        print("3. Exit")

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
            print("\nVault closed.")
            break

        else:
            print("\nPlease choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
    