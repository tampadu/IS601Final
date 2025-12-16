from fastapi import FastAPI, Request, Form, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db, User, Calculation, hash_password, verify_password

app = FastAPI(title="Calculations App")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# -----------------------------
# Helper to get logged-in user
# -----------------------------
def get_logged_in_user_id(request: Request):
    user_id = request.cookies.get("user_id")
    return int(user_id) if user_id else None


# -----------------------------
# Home / root
# -----------------------------
@app.get("/")
def home():
    return RedirectResponse("/login")


# -----------------------------
# Login
# -----------------------------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.hashed_password):
        response = RedirectResponse("/calculations-page", status_code=303)
        response.set_cookie(key="user_id", value=str(user.id))
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})


# -----------------------------
# Logout
# -----------------------------
@app.get("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("user_id")
    return response


# -----------------------------
# Registration
# -----------------------------
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(None),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists"})
    
    user = User(username=username, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/login", status_code=303)


# -----------------------------
# Profile Page
# -----------------------------
@app.get("/profile")
def profile_page(request: Request, db: Session = Depends(get_db)):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return RedirectResponse("/login")
    
    user = db.query(User).filter(User.id == user_id).first()
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": user.username, "email": user.email or ""}
    )


@app.post("/profile/update")
def update_profile(
    request: Request,
    username: str = Form(...),
    email: str = Form(None),
    db: Session = Depends(get_db)
):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return RedirectResponse("/login")

    user = db.query(User).filter(User.id == user_id).first()
    user.username = username
    user.email = email
    db.commit()
    return RedirectResponse("/profile", status_code=303)


@app.post("/profile/password")
def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user_id = get_logged_in_user_id(request)
    if not user_id:
        return RedirectResponse("/login")

    user = db.query(User).filter(User.id == user_id).first()
    if not verify_password(current_password, user.hashed_password):
        return RedirectResponse("/profile", status_code=303)

    if new_password != confirm_new_password:
        return RedirectResponse("/profile", status_code=303)

    user.hashed_password = hash_password(new_password)
    db.commit()
    return RedirectResponse("/profile", status_code=303)


# -----------------------------
# Calculations Page
# -----------------------------
@app.get("/calculations-page")
def calculations_page(request: Request):
    return templates.TemplateResponse("calculations.html", {"request": request})
