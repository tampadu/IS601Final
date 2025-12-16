# tests/test_schemas.py
import pytest
from app.schemas import CalculationCreate, UserCreate, UserLogin

def test_calculation_create_valid():
    data = {"a": 5, "b": 3, "type": "Add"}
    calc = CalculationCreate(**data)
    assert calc.a == 5
    assert calc.b == 3
    assert calc.type == "Add"

def test_calculation_create_invalid_type():
    data = {"a": 1, "b": 2, "type": "Invalid"}
    with pytest.raises(ValueError):
        CalculationCreate(**data)

def test_user_create_and_login():
    user_data = {"email": "a@b.com", "password": "mypassword"}
    user = UserCreate(**user_data)
    assert user.email == "a@b.com"

    login_data = {"email": "a@b.com", "password": "mypassword"}
    login = UserLogin(**login_data)
    assert login.password == "mypassword"
