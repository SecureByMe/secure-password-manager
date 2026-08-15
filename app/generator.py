import secrets
import string


def generate_password(length: int = 16) -> str:
    """Generate a strong random password."""

    if length < 12:
        raise ValueError(
            "Password length must be at least 12 characters."
        )

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+"

    characters = lowercase + uppercase + digits + symbols

    password_characters = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    password_characters.extend(
        secrets.choice(characters)
        for _ in range(length - 4)
    )

    secrets.SystemRandom().shuffle(password_characters)

    return "".join(password_characters)
