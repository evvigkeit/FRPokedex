from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import RedirectResponse

from app import db
from app.core.templates import templates
from app.core.oauth2scheme import COOKIE_SESSION_ID_KEY
from app.utils.security_util import check_session, delete_cookie

user = APIRouter()


@user.get("/profile/{username}")
def profile_get(request: Request, username: str):
    user = db.get_user_data(username)
    session_exists = check_session(request, username)
    if session_exists:
        return templates.TemplateResponse("profile.html", {"request": request, "username": user.username, "email": user.email, "phone": user.phone, "created": user.days_with_us})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated",)


@user.get("/sign_out")
def sign_out(request: Request):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    db.delete_session_from_db(session_id)
    delete_cookie(session_id)
    return RedirectResponse("/authorization")
