from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import Calculation, get_db

router = APIRouter()


def get_user_id(request: Request) -> int:
    return int(request.cookies.get("user_id"))


@router.post("/add")
def add_calculation(
    request: Request,
    a: float = Form(...),
    b: float = Form(...),
    type: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = get_user_id(request)

    if type == "add":
        result = a + b
    elif type == "subtract":
        result = a - b
    elif type == "multiply":
        result = a * b
    elif type == "divide":
        result = a / b if b != 0 else 0
    else:
        result = 0

    calculation = Calculation(
        user_id=user_id,
        a=a,
        b=b,
        type=type,
        result=result
    )

    db.add(calculation)
    db.commit()

    return RedirectResponse("/calculations-page", status_code=303)
