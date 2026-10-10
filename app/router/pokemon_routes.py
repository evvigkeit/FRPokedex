from fastapi import APIRouter, Request, Query, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated

from app.core.templates import templates
from app.db.db_crud.pokemon_tables import (get_pokemon_by_type, get_pokemons, get_pokemon_info, get_pokemon_weaknesses, insert_into_pokedex, check_in_pokedex, 
                                            delete_from_pokedex)
from app.models.user import User
from app.utils.security_util import get_user_by_session_id 


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
def pokemon_page_get(request: Request, pokemon_name, user: User = Depends(get_user_by_session_id)):
    pokemon_info = get_pokemon_weaknesses(get_pokemon_info(pokemon_name))
    
    caught_at = check_in_pokedex(user.id, pokemon_info.id)
    
    return templates.TemplateResponse("pokemon_info.html",{"request": request, "pokemon_info": pokemon_info, "caught_at": caught_at})


@pokemon.post("/pokedex/add")
def add_pokemon_to_pokedex(request: Request, pokemon_id: int = Form(), user: User = Depends(get_user_by_session_id)):
    insert_into_pokedex(user.id, pokemon_id)
    
    referer = request.headers.get("referer")
    
    if referer:
        return RedirectResponse(url=referer, status_code=303)
    return RedirectResponse(url="/", status_code=303)


@pokemon.post("/pokedex/delete")
def delete_pokemon_from_pokedex(request: Request, pokemon_id: int = Form(), user: User = Depends(get_user_by_session_id)):
    delete_from_pokedex(user.id, pokemon_id)
    
    referer = request.headers.get("referer")
    
    if referer:
        return RedirectResponse(url=referer, status_code=303)
    return RedirectResponse("/", status_code=303)