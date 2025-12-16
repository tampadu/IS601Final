from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal, get_db, hash_password, verify_password, init_db
from app.models import User
from app.calculations import add_calculation

app = FastAPI()

# --- Initialize database tables ---
init_db()

# --- Mount static folder for CSS, JS, images ---
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# --- Templates folder ---
templates = Jinja2Templates(directory="app/templates")

# --- Dependency ---
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def home():
    # Redirect to login page on startup
    return RedirectResponse("/login")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    hashed = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse("/login", status_code=303)

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db_session)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return {"detail": "Invalid credentials"}
    response = RedirectResponse("/calculations-page", status_code=303)
    response.set_cookie("user_id", str(user.id))
    return response

@app.get("/calculations-page", response_class=HTMLResponse)
def calculations_page(request: Request):
    return templates.TemplateResponse("calculations.html", {"request": request})

@app.post("/profile/update")
def update_profile(username: str = Form(...), email: str = Form(...), request: Request = None, db: Session = Depends(get_db_session)):
    user_id = int(request.cookies.get("user_id"))
    user = db.query(User).get(user_id)
    user.username = username
    user.email = email
    db.commit()
    return RedirectResponse("/profile", status_code=303)

@app.post("/profile/password")
def change_password(current_password: str = Form(...), new_password: str = Form(...), confirm_new_password: str = Form(...), request: Request = None, db: Session = Depends(get_db_session)):
    user_id = int(request.cookies.get("user_id"))
    user = db.query(User).get(user_id)
    if not verify_password(current_password, user.hashed_password) or new_password != confirm_new_password:
        return {"detail": "Invalid password change"}
    user.hashed_password = hash_password(new_password)
    db.commit()
    return RedirectResponse("/profile", status_code=303)

@app.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})
