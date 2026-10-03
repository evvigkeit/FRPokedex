from fastapi import APIRouter, Request, Query
from typing import Annotated

from app.core.templates import templates
from app.db.db_crud.pokemon_tables import get_pokemon_by_type, get_pokemons, get_pokemon_info, get_pokemon_weaknesses


pokemon = APIRouter()


@pokemon.get("/pokemons")
def login_get(request: Request, pokemon_name: str = '', pokemon_types: Annotated[list[str] | None, Query()] = None):
    if pokemon_types:
        pokemons = get_pokemon_by_type(pokemon_types)
    else:   
        pokemons = get_pokemons(pokemon_name)
    return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons": pokemons})

@pokemon.get("/pokemons/{pokemon_name}")
def login_get(request: Request, pokemon_name):
    pokemon_info = get_pokemon_weaknesses(get_pokemon_info(pokemon_name))
    return templates.TemplateResponse("pokemon_info.html",{"request": request, "pokemon_info": pokemon_info})