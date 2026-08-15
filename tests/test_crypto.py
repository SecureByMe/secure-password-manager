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

from app.crypto import derive_key, generate_salt, encrypt_data, decrypt_data


def test_encryption_and_decryption():
    password = "TestPassword123!"
    salt = generate_salt()

    key = derive_key(password, salt)

    original_data = b"My secret password data"

    encrypted_data, nonce = encrypt_data(original_data, key)

    decrypted_data = decrypt_data(
        encrypted_data,
        key,
        nonce
    )

    assert encrypted_data != original_data
    assert decrypted_data == original_data


def test_tampered_data_fails_decryption():
    password = "TestPassword123!"
    salt = generate_salt()

    key = derive_key(password, salt)

    original_data = b"My secret password data"

    encrypted_data, nonce = encrypt_data(original_data, key)

    tampered_data = bytearray(encrypted_data)
    tampered_data[0] ^= 1

    try:
        decrypt_data(bytes(tampered_data), key, nonce)
        assert False, "Tampered data should not decrypt"
    except Exception:
        pass
    
