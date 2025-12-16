# app/utils/calc_engine.py

from typing import Union

Number = Union[int, float]

ALLOWED_TYPES = ("Add", "Sub", "Multiply", "Divide")

def evaluate(a: Number, b: Number, op_type: str) -> float:
    """
    Evaluate a, b according to op_type.
    Allowed op_type values: "Add", "Sub", "Multiply", "Divide"
    Returns numeric result as float. Raises ValueError for invalid op_type or invalid operands.
    """
    if op_type not in ALLOWED_TYPES:
        raise ValueError(f"Invalid operation type: {op_type}")

    # Ensure inputs are numbers
    try:
        a_f = float(a)
        b_f = float(b)
    except Exception:
        raise ValueError("Operands must be numeric")

    if op_type == "Add":
        return a_f + b_f
    if op_type == "Sub":
        return a_f - b_f
    if op_type == "Multiply":
        return a_f * b_f
    if op_type == "Divide":
        if b_f == 0:
            raise ValueError("Division by zero")
        return a_f / b_f

    # safety fallback
    raise ValueError("Unsupported operation")
