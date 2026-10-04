from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from pwdlib import PasswordHash

from fastapi import HTTPException, status, Response, Request

from app.db.db_crud.session_tables import check_session_by_username, get_user_by_session_id_from_db
from app.models.user import Session, User
from app.core.oauth2scheme import SESSION_EXPIRE_MINUTES, COOKIE_SESSION_ID_KEY


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


def check_session(request: Request, username: str):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    print(session_id, 'session_id!!')
    if session_id:
        session_exists = check_session_by_username(session_id, username)
        if session_exists:
            return session_id
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated",)


def delete_cookie(cookie_key: str):
    response = Response()
    response.delete_cookie(cookie_key)
    return {"message": "Successful exit!"}
    
def get_user_by_session_id(request: Request) -> User:
    session = request.cookies.get(COOKIE_SESSION_ID_KEY)
    user = get_user_by_session_id_from_db(session)
    if not user:
        return None
    return user