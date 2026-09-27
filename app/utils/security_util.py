from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Response

from app import db
from app.models.user import Session
from app.core.oauth2scheme import SESSION_EXPIRE_MINUTES, COOKIE_SESSION_ID_KEY

from secrets import token_urlsafe



password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_session(user_name: str) -> Session:
    session_id = token_urlsafe(32)
    login = datetime.now(timezone.utc)
    expires = login + timedelta(minutes=SESSION_EXPIRE_MINUTES)
    return Session(user_name, session_id, login, expires)


def check_session(request: str, username: str):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    if session_id:
        session_exists = db.check_session_in_db(session_id, username)
        if session_exists:
            return session_id
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated",)


def delete_cookie(cookie_key: str):
    response = Response()
    response.delete_cookie(cookie_key)
    return {"message": "Successful exit!"}
    