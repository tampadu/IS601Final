# app/services.py
from sqlalchemy.orm import Session
from .models import Calculation
from .schemas import CalculationCreate

def create_calculation(db: Session, calc: CalculationCreate, user_id: int):
    """
    Creates a new Calculation record in the database for a specific user.

    Parameters:
        db: SQLAlchemy Session
        calc: CalculationCreate Pydantic model
        user_id: ID of the user who owns this calculation

    Returns:
        The created Calculation instance
    """
    # Compute result based on type
    operation = calc.type.lower()
    if operation == "add":
        result_value = calc.a + calc.b
    elif operation == "sub":
        result_value = calc.a - calc.b
    elif operation == "multiply":
        result_value = calc.a * calc.b
    elif operation == "divide":
        result_value = calc.a / calc.b if calc.b != 0 else 0
    else:
        result_value = 0

    # Create Calculation model instance
    calculation = Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=result_value,
        owner_id=user_id  # Make sure your Calculation model uses 'owner_id'
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation
