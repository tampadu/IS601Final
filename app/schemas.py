from pydantic import BaseModel, validator
from pydantic import BaseModel, EmailStr, constr

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: str

    @validator("type")
    def valid_type(cls, v):
        if v not in ("Add", "Sub", "Multiply", "Divide"):
            raise ValueError("Type must be Add, Sub, Multiply, or Divide")
        return v

    @validator("b")
    def no_zero_division(cls, v, values):
        if values.get("type") == "Divide" and v == 0:
            raise ValueError("Division by zero is not allowed")
        return v

class CalculationRead(BaseModel):
    id: int
    a: float
    b: float
    type: str
    result: float

    class Config:
        orm_mode = True

# For registration
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
