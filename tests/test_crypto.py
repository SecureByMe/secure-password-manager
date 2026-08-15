from app.crypto import derive_key, generate_salt


def test_key_derivation():
    password = "TestPassword123!"
    salt = generate_salt()

    key1 = derive_key(password, salt)
    key2 = derive_key(password, salt)

    assert key1 == key2
    assert len(key1) == 32


def test_different_password_produces_different_key():
    salt = generate_salt()

    key1 = derive_key("PasswordOne", salt)
    key2 = derive_key("PasswordTwo", salt)

    assert key1 != key2


def test_salt_is_random():
    salt1 = generate_salt()
    salt2 = generate_salt()

    assert salt1 != salt2
    assert len(salt1) == 16