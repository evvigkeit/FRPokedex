from fastapi import APIRouter, Request

from app import db
from app.core.templates import templates


pokemon = APIRouter()


@pokemon.get("/pokemons")
def login_get(request: Request):
    pokemons = db.get_pokemons()
    return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons": pokemons})

@pokemon.get("/pokemons/{pokemon_name}")
def login_get(request: Request, pokemon_name):
    pokemon = db.get_pokemon_info(pokemon_name)
    pokemon_info = db.get_pokemon_types(pokemon)
    return templates.TemplateResponse("pokemon_info.html",{"request": request, "pokemon_info": pokemon_info})