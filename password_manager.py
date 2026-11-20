from config import PASSWORDS_FILE
from storage import load_data, save_data

from encryption import (
    encrypt_password,
    decrypt_password
)

from password_generator import generate_password


def add_password(master_password, salt):
    records = load_data(PASSWORDS_FILE)

    website = input("Enter website: ").strip()
    username = input("Enter username/email: ").strip()

    if not website or not username:
        print("Website and username are required.")
        return

    print("1. Enter password manually")
    print("2. Generate strong password")

    choice = input("Choose option: ").strip()

    if choice == "1":
        import getpass
        password = getpass.getpass("Enter password: ")

    elif choice == "2":
        try:
            length = int(input("Password length (minimum 8): "))
            password = generate_password(length)
            print(f"Generated password: {password}")
        except ValueError as error:
            print(error)
            return

    else:
        print("Invalid choice.")
        return

    if not password:
        print("Password cannot be empty.")
        return

    encrypted = encrypt_password(
        password,
        master_password,
        salt
    )

    record = {
        "id": max(
            (item["id"] for item in records),
            default=0
        ) + 1,
        "website": website,
        "username": username,
        "encrypted_password": encrypted
    }

    records.append(record)
    save_data(PASSWORDS_FILE, records)

    print("Password saved successfully!")


def view_passwords(master_password, salt):
    records = load_data(PASSWORDS_FILE)

    if not records:
        print("No saved passwords.")
        return

    print("\nSAVED ACCOUNTS")

    for record in records:
        try:
            password = decrypt_password(
                record["encrypted_password"],
                master_password,
                salt
            )
        except Exception:
            password = "[Unable to decrypt]"

        print("-" * 45)
        print(f"ID: {record['id']}")
        print(f"Website: {record['website']}")
        print(f"Username: {record['username']}")
        print(f"Password: {password}")


def search_password(master_password, salt):
    records = load_data(PASSWORDS_FILE)

    search = input("Enter website to search: ").strip().lower()

    matches = [
        item for item in records
        if search in item["website"].lower()
    ]

    if not matches:
        print("No matching account found.")
        return

    for record in matches:
        try:
            password = decrypt_password(
                record["encrypted_password"],
                master_password,
                salt
            )
        except Exception:
            password = "[Unable to decrypt]"

        print("-" * 40)
        print(f"Website: {record['website']}")
        print(f"Username: {record['username']}")
        print(f"Password: {password}")


def update_password(master_password, salt):
    records = load_data(PASSWORDS_FILE)

    try:
        record_id = int(input("Enter account ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for record in records:
        if record["id"] == record_id:
            import getpass

            username = input(
                f"New username [{record['username']}]: "
            ).strip()

            if username:
                record["username"] = username

            new_password = getpass.getpass(
                "Enter new password (leave blank to keep current): "
            )

            if new_password:
                record["encrypted_password"] = encrypt_password(
                    new_password,
                    master_password,
                    salt
                )

            save_data(PASSWORDS_FILE, records)
            print("Account updated successfully!")
            return

    print("Account not found.")


def delete_password():
    records = load_data(PASSWORDS_FILE)

    try:
        record_id = int(input("Enter account ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    updated = [
        item for item in records
        if item["id"] != record_id
    ]

    if len(updated) == len(records):
        print("Account not found.")
        return

    save_data(PASSWORDS_FILE, updated)
    print("Account deleted successfully!")
