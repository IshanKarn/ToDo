from passlib.context import CryptContext
from app.crud import get_user_by_username

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate(username: str, password: str):
    """
    Returns user if authentication succeeds, else None
    """
    user = get_user_by_username(username)

    if not user:
        return None

    if not verify_password(password, user['password']):
        return None

    return user