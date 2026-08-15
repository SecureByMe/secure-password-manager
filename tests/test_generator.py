import string

import pytest

from app.generator import generate_password


def test_generated_password_has_requested_length():
    password = generate_password(20)

    assert len(password) == 20


def test_generated_password_contains_required_character_types():
    password = generate_password(20)

    assert any(character in string.ascii_lowercase for character in password)
    assert any(character in string.ascii_uppercase for character in password)
    assert any(character in string.digits for character in password)
    assert any(character in "!@#$%^&*()-_=+" for character in password)


def test_password_length_must_be_at_least_twelve():
    with pytest.raises(ValueError):
        generate_password(11)
        