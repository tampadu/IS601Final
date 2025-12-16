# tests/test_models.py
from app.models import User
from sqlalchemy import Column, Integer, String

def test_user_model_fields():
    assert hasattr(User, "id")
    assert hasattr(User, "username")
    assert hasattr(User, "hashed_password")
