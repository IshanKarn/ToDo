from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.database import get_connection
from app.auth import create_access_token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/login")
def login(username: str, password: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user[0]})
    return {"access_token": token, "token_type": "bearer"}