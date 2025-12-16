# app/calculations.py
from sqlalchemy.orm import Session
from app.models import User, Calculation

def add_calculation(request, a: float, b: float, type: str, db: Session):
    """Add a calculation for the current user."""
    user_id = int(request.cookies.get("user_id"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise Exception("User not found")

    if type.lower() == "add":
        result = a + b
    elif type.lower() == "subtract":
        result = a - b
    elif type.lower() == "multiply":
        result = a * b
    elif type.lower() == "divide":
        result = a / b if b != 0 else 0
    else:
        raise ValueError("Invalid calculation type")

    calc = Calculation(user_id=user.id, a=a, b=b, type=type, result=result)
    db.add(calc)
    db.commit()
    db.refresh(calc)
    return calc
