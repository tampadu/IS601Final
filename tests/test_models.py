# tests/test_models.py
from app.models import User, Calculation

def test_user_model_fields():
    user_fields = ["id", "username", "email", "hashed_password", "calculations"]
    for field in user_fields:
        assert hasattr(User, field)

def test_calculation_model_fields():
    calc_fields = ["id", "user_id", "a", "b", "type", "result", "created_at", "updated_at", "user"]
    for field in calc_fields:
        assert hasattr(Calculation, field)
