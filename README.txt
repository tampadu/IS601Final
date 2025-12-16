IS601Final – Calculator Application
Overview
This project is a FastAPI web application that allows users to perform calculations, store calculation
history, and manage user accounts. The app features:
•
•
•
•
•
User registration, login, and profile management.
CRUD operations for calculations.
Password hashing and authentication.
SQLite database integration with SQLAlchemy ORM.
Automated unit and integration tests with Pytest.
Features
Authentication
•
•
•
User registration and login
Password hashing using bcrypt
Profile update and password change
Calculations
•
•
•
Add, subtract, multiply, and divide
Store calculation history per user
View all previous calculations on a dedicated page
Database
•
•
•
SQLite database ( test.db for development/testing)
SQLAlchemy ORM models for User and Calculation
Automatic table creation
API Endpoints
Endpoint Method Description
/register POST Register a new user
/login POST Login a user
/calculations-page GET View calculation history
/profile/update POST Update user profile
/profile/password POST Change user password
1
Endpoint Method Description
/add-calculation POST Add a new calculation
Project Structure
IS601Final/
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── services.py
│ ├── calculations.py
│ └── auth.py
├── tests/
│ ├── test_auth.py
│ ├── test_calculations.py
│ ├── test_database.py
│ ├── test_main.py
│ ├── test_models.py
│ ├── test_schemas.py
│ └── test_services.py
├── requirements.txt
└── README.md
Installation
1.
Clone the repository
git clone https://github.com/tampadu/IS601Final
cd IS601Final
1.
Create a virtual environment and activate it
2
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
1.
Install dependencies
pip install -r requirements.txt
Database Setup
The app uses SQLite. Tables are automatically created when the app runs:
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
Running the Application
uvicorn app.main:app --reload
•
Navigate to http://127.0.0.1:8000 to access the app.
Running Tests
The project uses pytest for testing:
PYTHONPATH=$(pwd) pytest -v
•
•
•
•
•
•
•
Tests use a temporary SQLite database to ensure isolation.
Tests cover:
Authentication ( test_auth.py )
Database operations ( test_database.py )
Calculations ( test_calculations.py, test_services.py )
API endpoints ( test_main.py )
Models and schemas ( test_models.py, test_schemas.py )
3
Security
•
•
•
Passwords are hashed using bcrypt ( passlib library).
User sessions managed via cookies.
All sensitive operations require authentication.
Dependencies
•
•
•
•
•
FastAPI
SQLAlchemy
Passlib
Pytest
Uvicorn