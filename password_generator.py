import secrets
import string


def generate_password(length=16):
    if length < 8:
        raise ValueError("Password length must be at least 8.")

    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*()-_=+"
    )

    while True:
        password = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%^&*()-_=+" for c in password)
        ):
            return password
