from fastapi import APIRouter, Request

from app import db
from app.core.templates import templates


user = APIRouter()


@user.get("/profile/{username}")
def profile_get(request: Request, username: str):
    user = db.get_user_data(username)
    return templates.TemplateResponse("profile.html", {"request": request, "username": user.username, "email": user.email, "phone": user.phone, "created": user.days_with_us})
