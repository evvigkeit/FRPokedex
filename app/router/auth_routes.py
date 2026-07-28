from fastapi import APIRouter, Request

from app import db
from app.models.user import User
from app.models.pydantic_models import AuthForm, RegForm
import app.utils.auth_util as auth_util
from app.core.templates import templates


auth = APIRouter()

@auth.get("/authorization")
def login_get(request: Request):
    return templates.TemplateResponse("authorization/authorization.html",{"request": request})


@auth.post("/authorization")
def login_post(auth_user: AuthForm):
    auth_result = auth_util.validate_auth(User(username=auth_user.username, password=auth_user.password))
    return auth_result


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
