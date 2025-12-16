# tests/test_auth.py
import pytest
from app.auth import get_password_hash, verify_password, create_access_token

def test_password_hash_and_verify():
    password = "secret123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)

def test_create_access_token():
    data = {"sub": "user1"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0
