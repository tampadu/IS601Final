# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal, User, hash_password

client = TestClient(app)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def test_user():
    db = SessionLocal()
    user = User(username="mainuser", email="main@example.com", hashed_password=hash_password("password"))
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user

def test_register_and_login(test_user):
    # Register new user
    response = client.post("/register", data={"username": "newuser2", "email": "new2@example.com", "password": "password"})
    assert response.status_code == 303

    # Login with correct password
    response = client.post("/login", data={"username": "newuser2", "password": "password"})
    assert response.status_code == 303
    assert "user_id" in response.cookies

    # Login with wrong password
    response = client.post("/login", data={"username": "newuser2", "password": "wrong"})
    assert response.status_code == 200
    assert "Invalid credentials" in response.text

def test_calculations_page():
    response = client.get("/calculations-page")
    assert response.status_code == 200
    assert "<h1>My Calculations</h1>" in response.text

def test_profile_update_and_password_change(test_user):
    client.cookies.set("user_id", str(test_user.id))

    # Update profile
    response = client.post("/profile/update", data={"username": "updateduser", "email": "updated@example.com"})
    assert response.status_code == 303

    # Change password
    response = client.post("/profile/password", data={"current_password": "password", "new_password": "newpass", "confirm_new_password": "newpass"})
    assert response.status_code == 303
