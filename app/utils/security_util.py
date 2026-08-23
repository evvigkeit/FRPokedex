import jwt
from jwt.exceptions import InvalidTokenError

import os
from pwdlib import PasswordHash
from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

from app import db
from app.models.pydantic_models import TokenData
from app.core.oauth2scheme import oauth2scheme, ACCESS_TOKEN_EXPIRE_MINUTES


password_hash = PasswordHash.recommended()


def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt


def access_token_expires():
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

def get_current_user(token: Annotated[str, Depends(oauth2scheme)]):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}   # specification requirement
        )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    
    except InvalidTokenError:
        raise credentials_exception
    
    user = db.get_user_data(username=token_data.username)
    if not user:
        raise credentials_exception
    return user
