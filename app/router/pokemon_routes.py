from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
from typing import Annotated

from app.core.templates import templates
from app.db.db_crud.pokemon_tables import get_pokemon_by_type, get_pokemons, get_pokemon_info, get_pokemon_weaknesses


pokemon = APIRouter()


@pokemon.get("/pokemons")
def filter_pokemons_get(request: Request, pokemon_name: Annotated[str, Query()] = '', pokemon_types: Annotated[list[str] | None, Query()] = None):
    if not pokemon_types and not pokemon_name:
        pokemons = get_pokemons('')
        return templates.TemplateResponse("pokemons.html",{"request": request, "pokemons": pokemons})
    
    if pokemon_types:
        pokemons = get_pokemon_by_type(pokemon_types)
    elif pokemon_name:   
        pokemons = get_pokemons(pokemon_name)
    return JSONResponse({"pokemons": pokemons})



@pokemon.get("/pokemons/{pokemon_name}")
def pokemon_page_get(request: Request, pokemon_name):
    pokemon_info = get_pokemon_weaknesses(get_pokemon_info(pokemon_name))
    return templates.TemplateResponse("pokemon_info.html",{"request": request, "pokemon_info": pokemon_info})