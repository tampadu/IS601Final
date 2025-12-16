# tests/test_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal, hash_password
from app.models import User
from app.calculations import add_calculation
from sqlalchemy.orm import Session
import uuid

# --- Fixture to create a fresh test client ---
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# --- Fixture to reset the database before each test ---
@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- Fixture to create a test user ---
@pytest.fixture
def test_user():
    db = SessionLocal()
    email = f"test_{uuid.uuid4().hex}@example.com"
    user = User(username="testuser", email=email, hashed_password=hash_password("password"))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

# --- Integration Tests ---

def test_register(client):
    email = f"register_{uuid.uuid4().hex}@example.com"
    response = client.post(
        "/register",
        data={"username": "newuser", "email": email, "password": "secret"},
        allow_redirects=False
    )
    assert response.status_code == 303
    assert "/login" in response.headers["location"]

def test_login(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user.username, "password": "password"},
        allow_redirects=False
    )
    assert response.status_code == 303
    assert str(test_user.id) in response.cookies.get("user_id", "")

def test_calculations_page(client):
    response = client.get("/calculations-page")
    assert response.status_code == 200
    assert "<h1>My Calculations</h1>" in response.text

def test_add_calculation(client, test_user):
    # Simulate request object with cookies
    class DummyRequest:
        def __init__(self, user_id):
            self.cookies = {"user_id": str(user_id)}
    request = DummyRequest(test_user.id)

    # Add a calculation
    from sqlalchemy.orm import Session
    db: Session = SessionLocal()
    calc = add_calculation(request, a=10, b=5, type="Add", db=db)

    assert calc.id is not None
    assert calc.a == 10
    assert calc.b == 5
    assert calc.type.lower() == "add"
    assert calc.result == 15

    db.close()

def test_profile_update(client, test_user):
    # Simulate request object with cookies
    class DummyRequest:
        def __init__(self, user_id):
            self.cookies = {"user_id": str(user_id)}
    request = DummyRequest(test_user.id)

    response = client.post(
        "/profile/update",
        data={"username": "updateduser", "email": f"updated_{uuid.uuid4().hex}@example.com"},
        cookies=request.cookies,
        allow_redirects=False
    )
    assert response.status_code == 303

def test_password_change(client, test_user):
    class DummyRequest:
        def __init__(self, user_id):
            self.cookies = {"user_id": str(user_id)}
    request = DummyRequest(test_user.id)

    response = client.post(
        "/profile/password",
        data={
            "current_password": "password",
            "new_password": "newpass",
            "confirm_new_password": "newpass"
        },
        cookies=request.cookies,
        allow_redirects=False
    )
    assert response.status_code == 303
