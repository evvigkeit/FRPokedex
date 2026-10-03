from typing import Annotated

from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from app.db.db_crud.session_tables import add_session_data
from app.db.db_crud.user_tables import create_user
from app.core.templates import templates
from app.core.oauth2scheme import COOKIE_SESSION_ID_KEY
from app.models.user import User
from app.models.pydantic_models import RegForm, ApiResponse
from app.utils import auth_util, security_util
from app.utils.security_util import check_session


auth = APIRouter()


@auth.post("/session")
def auth_login_set_cookie(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> ApiResponse:
    curr_user = User(username=form_data.username, password=form_data.password)
    auth_result = auth_util.validate_auth(curr_user)
    
    if not auth_result.success:
        return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(auth_result),
    )
    response = JSONResponse({"success": True})
    
    try:
        check_session(request, curr_user.username)
        
    except HTTPException:
        session_data = security_util.create_session(curr_user.username)   
        response.set_cookie(COOKIE_SESSION_ID_KEY, session_data.session_id, expires=session_data.expires, httponly=True)
        add_session_data(session_data)
        print("COOKIES", session_data)
    return response
    
    
@auth.get("/authorization")
def login_get(request: Request):
    return templates.TemplateResponse("authorization/authorization.html", {"request": request})


@auth.get("/registration")
def reg_get(request: Request):
    return templates.TemplateResponse("authorization/registration.html", {"request": request})


@auth.post("/registration")
def reg_post(reg_user: RegForm):
    new_user = User(username=reg_user.username, password=reg_user.password, email=reg_user.email, phone=reg_user.phone)
    reg_result = auth_util.validate_reg(new_user)  
    if reg_result.success:
        create_user(new_user)
        return reg_result
    
    return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(reg_result),
        )
