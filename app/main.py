from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import db
from app.models.user import User
from app.models.pydantic_models import AuthForm, RegForm
import app.utils.auth_util as auth_util


templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
We need it here to process CSS files which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/authorization")
def login_get(request: Request):
    return templates.TemplateResponse("authorization/authorization.html",{"request": request})


@app.post("/authorization")
def login_post(request: Request, auth_user: AuthForm):
    result = auth_util.validate_auth(User(username=auth_user.username, password=auth_user.password))
    return result
    
    
    if auth_err:
        return templates.TemplateResponse("authorization/authorization.html",{"request": request, "password_err": auth_err})  # 1 - wrong password, 2 - user not exists
    return RedirectResponse(f"/profile/{auth_user.username}", status_code=303)


@app.get("/registration")
def reg_get(request: Request):
    return templates.TemplateResponse("authorization/registration.html", {"request": request})

@app.post("/registration")
def reg_post(request: Request, reg_user: RegForm):
    new_user = User(username=reg_user.username, password=reg_user.password, email=reg_user.email, phone=reg_user.phone)

    reg_err = auth_util.validate_reg(new_user)  
    if reg_err:
        return templates.TemplateResponse("authorization/registration.html",{"request": request, "registration_err": reg_err})

    if reg_user.password != reg_user.ch_password:
        return templates.TemplateResponse("authorization/registration.html",{"request": request, "registration_err": "password"})
    db.create_user(new_user)
    return RedirectResponse(f"/profile/{new_user.username}", status_code=303)


@app.get("/profile/{username}")
def profile_get(request: Request, username: str):
    user = db.get_user_data(username)
    return templates.TemplateResponse("profile.html", {"request": request, "username": user.username, "email": user.email, "phone": user.phone, "created": user.days_with_us})