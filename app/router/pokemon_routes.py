from fastapi import APIRouter, Request

from app import db
from app.core.templates import templates


pokemon = APIRouter()


@pokemon.get("/pokemons")
def login_get(request: Request):
    pokemons = db.get_pokemons()
    return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons": pokemons})