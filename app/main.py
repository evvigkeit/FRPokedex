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
def login_post(auth_user: AuthForm):
    auth_result = auth_util.validate_auth(User(username=auth_user.username, password=auth_user.password))
    return auth_result


@app.get("/registration")
def reg_get(request: Request):
    return templates.TemplateResponse("authorization/registration.html", {"request": request})

@app.post("/registration")
def reg_post(reg_user: RegForm):
    new_user = User(username=reg_user.username, password=reg_user.password, email=reg_user.email, phone=reg_user.phone)
    reg_result = auth_util.validate_reg(new_user, reg_user.ch_password)  
    return reg_result


@app.get("/profile/{username}")
def profile_get(request: Request, username: str):
    user = db.get_user_data(username)
    return templates.TemplateResponse("profile.html", {"request": request, "username": user.username, "email": user.email, "phone": user.phone, "created": user.days_with_us})