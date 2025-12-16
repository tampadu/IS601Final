# tests/test_database.py
from app.models import User, Calculation, hash_password, verify_password
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import sessionmaker

TestingSessionLocal = SessionLocal

def test_user_password_hashing():
    password = "mypassword"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpass", hashed)

def test_create_user_and_calculation():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    user = User(username="dbuser", email="db@example.com", hashed_password=hash_password("pass"))
    db.add(user)
    db.commit()
    db.refresh(user)
    calc = Calculation(user_id=user.id, a=1, b=2, type="Add", result=3)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    assert calc.user_id == user.id
    db.close()
