from sqlalchemy.orm import Session
from . import models, schemas

def create_calculation(db: Session, calc: schemas.CalculationCreate):
    result = models.Calculation(
        a=calc.a,
        b=calc.b,
        type=calc.type,
        result=models.Calculation(a=calc.a, b=calc.b, type=calc.type).compute_result()
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
