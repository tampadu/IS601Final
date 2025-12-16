import pytest
from app.services import create_calculation
from app.schemas import CalculationCreate
from app.database import Calculation, User

def test_create_calculation(db_session):
    # First, create a test user
    user = User(username="testuser", hashed_password="hashed")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create a calculation schema
    calc_schema = CalculationCreate(a=10, b=5, type="Add")
    
    # Use the service function
    calculation = create_calculation(db_session, calc_schema)
    
    # Check that calculation was saved
    assert calculation.id is not None
    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == "Add"
    assert calculation.result == 15  # 10 + 5
