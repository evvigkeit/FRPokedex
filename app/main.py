from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request

import connect_db as db

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

We need it here to process CSS files which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

@app.get("/login")
def login_page():
    return FileResponse("app/frontend/authorization.html")  # requesting the data from the source

@app.post("/authorized")
def login(request: Request, username: str = Form(), password: str = Form()):
    db.add_user_data(username, password)
    return templates.TemplateResponse(request, "authorized.html", {"username": username})