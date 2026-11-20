import os
import getpass

from config import MASTER_FILE, PASSWORDS_FILE
from storage import load_data, save_data

from encryption import (
    create_master,
    verify_master
)

from password_manager import (
    add_password,
    view_passwords,
    search_password,
    update_password,
    delete_password
)


def authenticate():
    master_data = load_data(MASTER_FILE, default=None)

    if not master_data:
        print("Create your master password.")

        password = getpass.getpass("New master password: ")
        confirm = getpass.getpass("Confirm master password: ")

        if len(password) < 8:
            print("Master password must contain at least 8 characters.")
            return None

        if password != confirm:
            print("Passwords do not match.")
            return None

        master_data = create_master(password)
        save_data(MASTER_FILE, master_data)

        print("Master password created successfully!")

    else:
        password = getpass.getpass("Enter master password: ")

        if not verify_master(password, master_data):
            print("Incorrect master password.")
            return None

    import base64

    salt = base64.b64decode(master_data["salt"])

    return password, salt


def main():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(PASSWORDS_FILE):
        save_data(PASSWORDS_FILE, [])

    credentials = authenticate()

    if credentials is None:
        return

    master_password, salt = credentials

    while True:
        print("\n================================")
        print("     PERSONAL PASSWORD MANAGER")
        print("================================")

        print("1. Add Password")
        print("2. View All Passwords")
        print("3. Search Password")
        print("4. Update Password")
        print("5. Delete Password")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_password(master_password, salt)

        elif choice == "2":
            view_passwords(master_password, salt)

        elif choice == "3":
            search_password(master_password, salt)

        elif choice == "4":
            update_password(master_password, salt)

        elif choice == "5":
            delete_password()

        elif choice == "6":
            print("Password Manager closed.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
