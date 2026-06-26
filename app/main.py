from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import db
from app.models.user import User
import app.utils.auth_util as auth_util

from datetime import datetime


templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.
We need it here to process CSS files which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="app/styles"), name="static")

@app.get("/authorization")
def login_get(request: Request):
    return templates.TemplateResponse("authorization/authorization.html",{"request": request})

@app.post("/authorization")
def login_post(request: Request, username: str = Form(), password: str = Form()):
    auth_err = auth_util.validate_auth(User(username=username, password=password))
    
    if auth_err:
        return templates.TemplateResponse("authorization/authorization.html",{"request": request, "password_err": auth_err})  # 1 - wrong password, 2 - user not exists
    return RedirectResponse(f"/profile/{username}", status_code=303)


@app.get("/registration")
def reg_get(request: Request):
    return templates.TemplateResponse("authorization/registration.html", {"request": request})

@app.post("/registration")
def reg_post(request: Request, username: str = Form(), email: str = Form(), phone: str = Form(), password: str = Form(), ch_password: str = Form()):
    new_user = User(username=username, password=password, email=email, phone=phone)
    reg_err = auth_util.validate_reg(new_user)
    
    if reg_err:
        return templates.TemplateResponse("authorization/registration.html",{"request": request, "registration_err": reg_err})

    if password != ch_password:
        return templates.TemplateResponse("authorization/registration.html",{"request": request, "registration_err": "password"})
    db.create_user(new_user)
    return RedirectResponse(f"/profile/{username}", status_code=303)



@app.get("/profile/{username}")
def profile_get(request: Request, username: str):
    user = db.get_user_data(username)
    return templates.TemplateResponse("profile.html", {"request": request, "username": user.username, "email": user.email, "phone": user.phone, "created": user.days_with_us})