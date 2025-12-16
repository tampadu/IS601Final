# README
# Calculation App

A FastAPI-based application that models basic arithmetic operations using SQLAlchemy and Pydantic. This project demonstrates robust data validation, polymorphic logic with a factory pattern, unit and integration testing, and Docker-based CI/CD.

---

## Features

- SQLAlchemy `Calculation` model with fields for `a`, `b`, `type`, and `result`.
- Pydantic schemas for input validation (`CalculationCreate`) and output serialization (`CalculationRead`).
- Factory pattern for dynamically handling different calculation types (`Add`, `Sub`, `Multiply`, `Divide`).
- Unit and integration tests with pytest.
- CI/CD workflow using GitHub Actions.
- Dockerized for consistent development and deployment environments.

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/tampadu/IS601Module11
cd calculation-app
Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
pip install -r requirements.txt
Configure PostgreSQL:
Ensure PostgreSQL is running locally.
Update app/database.py with your database credentials if necessary.
Running Locally
uvicorn app.main:app --reload
The app will be accessible at http://localhost:8000.
(Note: Endpoints are minimal since this module focuses on modeling and validation.)
Testing
Run all unit and integration tests:
pytest -v
Integration tests use a PostgreSQL database; Docker can be used to spin up a local test database.
Docker
Build and run the application with Docker:
docker build -t calculation-app .
docker run -p 8000:8000 calculation-app