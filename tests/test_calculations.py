# tests/test_calculations.py
import pytest
from app.models import User, Calculation
from app.calculations import add_calculation

class DummyRequest:
    def __init__(self, user_id):
        self.cookies = {"user_id": str(user_id)}

def test_add_calculation(db_session):
    user = User(username="calcuser", email="calc@example.com", hashed_password="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    request = DummyRequest(user.id)
    calc = add_calculation(request, a=10, b=5, type="add", db=db_session)
    assert calc.result == 15
    assert calc.user_id == user.id
