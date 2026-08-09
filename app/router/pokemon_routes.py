from fastapi import APIRouter, Request, Query
from typing import Annotated

from app import db
from app.core.templates import templates


pokemon = APIRouter()


@pokemon.get("/pokemons")
def login_get(request: Request, pokemon_name: str = '', pokemon_types: Annotated[list[str] | None, Query()] = None):
    if pokemon_types:
        pokemons = db.get_pokemon_by_type(pokemon_types)
    else:   
        pokemons = db.get_pokemons(pokemon_name)
    return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons": pokemons})

@pokemon.get("/pokemons/{pokemon_name}")
def login_get(request: Request, pokemon_name):
    pokemon_info = db.get_pokemon_weaknesses(db.get_pokemon_info(pokemon_name))
    return templates.TemplateResponse("pokemon_info.html",{"request": request, "pokemon_info": pokemon_info})