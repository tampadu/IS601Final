# tests/test_auth.py
from app.database import hash_password, verify_password
import pytest

def test_password_hash_and_verify():
    password = "secret123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)
