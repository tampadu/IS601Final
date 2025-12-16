# app/services.py
from sqlalchemy.orm import Session
from . import models, schemas

def create_calculation(db: Session, calc: schemas.CalculationCreate):
    """
    Creates a new Calculation record in the database.

    Parameters:
        db: SQLAlchemy Session
        calc: CalculationCreate Pydantic model

    Returns:
        The created Calculation instance
    """
    # Compute result based on type
    if calc.type.lower() == "add":
        result_value = calc.a + calc.b
    elif calc.type.lower() == "sub":
        result_value = calc.a - calc.b
    elif calc.type.lower() == "multiply":
        result_value = calc.a * calc.b
    elif calc.type.lower() == "divide":
        result_value = calc.a / calc.b if calc.b != 0 else 0
    else:
        result_value = 0

    # Create Calculation model instance
    calculation = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=result_value,
        user_id=getattr(calc, "user_id", None)  # Optional, if you track user
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation
