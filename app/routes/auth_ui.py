from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import get_connection
from app.auth import create_access_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

from app.security import hash_password

@router.get("/register")
def login_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_user(
    username: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=%s",
        (username,)
    )
    if cur.fetchone():
        conn.close()
        return RedirectResponse("/register?error=exists", status_code=302)

    if len(password) < 8:
        return RedirectResponse("/register?error=weak", status_code=302)

    hashed_password = hash_password(password)

    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
        (username, hashed_password)
    )

    user_id = cur.fetchone()[0]
    conn.commit()
    conn.close()

    token = create_access_token({"user_id": user_id})
    response = RedirectResponse("/", status_code=302)
    response.set_cookie("access_token", token, httponly=True)
    return response

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

from app.security import verify_password

@router.post("/login")
def login_user(
    username: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, password FROM users WHERE username=%s",
        (username,)
    )
    user = cur.fetchone()
    conn.close()

    if not user or not verify_password(password, user[1]):
        return RedirectResponse("/login?error=1", status_code=302)

    token = create_access_token({"user_id": user[0]})
    response = RedirectResponse("/", status_code=302)
    response.set_cookie("access_token", token, httponly=True)
    return response
