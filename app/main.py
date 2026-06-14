from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import connect_db as db

app = FastAPI()

'''
"Mounting" means adding a complete "independent" application in a specific path, that then takes care of handling all the sub-paths.

We need it here to process CSS files which are connected to the main HTML file.
'''
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/login")
def login_page():
    return FileResponse("frontend/authorization.html")  # requesting the data from the source

@app.post("/authorized")
def login(username: str = Form(), password: str = Form()):
    db.add_user_data(username, password)
    return {"username": username,
            "password": password}