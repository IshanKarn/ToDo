from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import get_connection
from app.auth import create_access_token
from app.security import authenticate

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

from app.security import hash_password

@router.get("/register")
def register_page(request: Request):
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
def login_user(username: str = Form(...), password: str = Form(...)):
    user = authenticate(username, password)
    if not user:
        return RedirectResponse("/login?error=invalid", status_code=302)

    token = create_access_token({"user_id": user["id"]})

    response = RedirectResponse("/", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        path="/",
        samesite="lax"
    )
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    return response