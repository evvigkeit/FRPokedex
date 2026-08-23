from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import db
from app.models.user import User
from app.models.pydantic_models import RegForm, Token
from app.utils import auth_util, security_util
from app.core.templates import templates


auth = APIRouter()


@auth.post("/token")
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    curr_user = User(username=form_data.username, password=form_data.password)
    auth_result = auth_util.validate_auth(curr_user)
    if not auth_result.success:
        return auth_result
    
    access_token = security_util.create_access_token(data={"sub": curr_user.username}, expires_delta=security_util.access_token_expires())
    return Token(access_token=access_token, token_type="bearer")


@auth.get("/authorization")
def login_get(request: Request):
    return templates.TemplateResponse("authorization/authorization.html",{"request": request})


@auth.post("/authorization")
def login_post(current_user: Annotated[User, Depends(security_util.get_current_user)]):
    return current_user


@auth.get("/registration")
def reg_get(request: Request):
    return templates.TemplateResponse("authorization/registration.html", {"request": request})


@auth.post("/registration")
def reg_post(reg_user: RegForm):
    new_user = User(username=reg_user.username, password=reg_user.password, email=reg_user.email, phone=reg_user.phone)
    reg_result = auth_util.validate_reg(new_user)  
    if reg_result.success:
        db.create_user(new_user)
    return reg_result
