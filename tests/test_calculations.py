# tests/test_calculations.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, User, Calculation
from app.calculations import add_calculation
from fastapi import Request

# Setup test DB
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_calc.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture
def test_user(db_session):
    user = User(username="calcuser", email="calc@example.com", hashed_password="fakehash")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

class DummyRequest:
    def __init__(self, user_id):
        self.cookies = {"user_id": str(user_id)}

def test_add_calculation(db_session, test_user):
    request = DummyRequest(test_user.id)
    response = add_calculation(request, a=10, b=5, type="add", db=db_session)
    calc = db_session.query(Calculation).filter(Calculation.user_id == test_user.id).first()
    assert calc.result == 15
    assert response.status_code == 303
