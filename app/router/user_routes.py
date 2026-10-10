from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse

from app.core.templates import templates
from app.core.oauth2scheme import COOKIE_SESSION_ID_KEY
from app.db.db_crud.pokemon_tables import get_from_pokedex
from app.db.db_crud.session_tables import delete_session_from_db
from app.models.user import User
from app.utils.security_util import delete_cookie, get_user_by_session_id


user = APIRouter()


@user.get("/profile/{username}")
def profile_get(request: Request, user: User = Depends(get_user_by_session_id)):
    if user:
        pokedex = get_from_pokedex(user.id)
        return templates.TemplateResponse("profile.html", {"request": request, "user": user, "pokedex": pokedex})
    return RedirectResponse("/authorization")


@user.get("/profile")
def profile_post(user: User = Depends(get_user_by_session_id)):
    if user:
        return RedirectResponse(f"/profile/{user.username}")
    return RedirectResponse("/authorization")


@user.get("/sign_out")
def sign_out(request: Request):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    delete_session_from_db(session_id)
    delete_cookie(session_id)
    return RedirectResponse("/authorization")
