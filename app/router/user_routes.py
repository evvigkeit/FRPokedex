from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse

from app import db
from app.core.templates import templates
from app.core.oauth2scheme import COOKIE_SESSION_ID_KEY
from app.models.user import User
from app.utils.security_util import check_session, delete_cookie, get_user_by_session_id

user = APIRouter()


@user.get("/profile/{username}")
def profile_get(request: Request, username: str):
    try:
        user = get_user_by_session_id(request)
        return templates.TemplateResponse("profile.html", {"request": request, "username": user.username, "email": user.email, "phone": user.phone, "created": user.days_with_us})

    except HTTPException:
        return RedirectResponse("/authorization")


@user.get("/profile")
def profile_post(user: User = Depends(get_user_by_session_id)):
    if type(user) is not User:
        return RedirectResponse("/authorization")
    return RedirectResponse(f"/profile/{user.username}")


@user.get("/sign_out")
def sign_out(request: Request):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    db.delete_session_from_db(session_id)
    delete_cookie(session_id)
    return RedirectResponse("/authorization")
