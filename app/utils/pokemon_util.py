from fastapi import Request

from app.core.oauth2scheme import COOKIE_SESSION_ID_KEY
from app.db.db_crud.pokemon_tables import insert_into_pokedex
from app.db.db_crud.session_tables import get_user_by_session_id_from_db


def add_pokemon_to_pokedex(request: Request, pokemon_id: int):
    session_id = request.cookies.get(COOKIE_SESSION_ID_KEY)
    user = get_user_by_session_id_from_db(session_id)
    
    insert_into_pokedex(user.id, pokemon_id)
