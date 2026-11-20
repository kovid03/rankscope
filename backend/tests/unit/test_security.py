import pytest
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token


def test_password_hashing():
    raw = "MySuperSecretPassword123!"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_password_long_truncation():
    raw_long = "A" * 150
    hashed = hash_password(raw_long)
    assert verify_password(raw_long, hashed) is True
    assert verify_password("A" * 72, hashed) is True


def test_jwt_token_creation_and_decoding():
    data = {"sub": "123", "email": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "123"
    assert decoded["email"] == "test@example.com"
    assert decoded["type"] == "access"


def test_jwt_invalid_token():
    assert decode_access_token("invalid.token.structure") is None
