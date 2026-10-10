import math
from datetime import datetime

from app.db.connection import get_db_cursor
from app.models.pokemon import Pokemon


def get_pokemons(pokemon_name: str) -> list:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT pokemon_name, file_name FROM pokemon_basic_info WHERE pokemon_name ILIKE %s;", ('%' + pokemon_name + '%',))
        pokemons = cursor.fetchall()
        return pokemons


def get_pokemon_by_type(pokemon_types: list) -> list:
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT pokemon_name, file_name, COUNT(*) FROM pokemon_types 
                            JOIN all_types ON pokemon_types.type_id = all_types.type_id
                            JOIN pokemon_basic_info ON pokemon_basic_info.pokemon_id = pokemon_types.pokemon_id
                            WHERE type_name IN %s
                            GROUP BY pokemon_name, file_name
                            HAVING COUNT(*) = %s""", (tuple(pokemon_types), len(pokemon_types)))
        pokemons = cursor.fetchall()
        pokemons = list(map(lambda x: x[:-1], pokemons))
        return pokemons


def get_pokemon_info(pokemon_name: str) -> Pokemon:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM pokemon_basic_info WHERE pokemon_name = %s;", (pokemon_name,))
        pokemon_info = cursor.fetchone()
        return Pokemon(*pokemon_info)


def get_pokemon_types(pokemon: Pokemon) -> Pokemon:
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT type_name FROM pokemon_types
                            JOIN all_types ON pokemon_types.type_id = all_types.type_id
                            JOIN pokemon_basic_info ON pokemon_basic_info.pokemon_id = pokemon_types.pokemon_id
                            WHERE pokemon_name = %s""", (pokemon.name,))
        pokemon_types = cursor.fetchall()
        pokemon.types = tuple(map(lambda x: x[0], pokemon_types))
        return pokemon


def get_pokemon_weaknesses(pokemon: Pokemon) -> Pokemon:
    with get_db_cursor() as cursor:
        if not pokemon.types:
            pokemon = get_pokemon_types(pokemon)
        
        cursor.execute("""WITH Spec_weaknesses AS (
                                SELECT defender_type, attacker_type, multiplier  FROM type_weaknesses
                                WHERE defender_type IN (SELECT type_id FROM all_types WHERE type_name IN %s)
                                )
                        SELECT type_name, ARRAY_AGG(multiplier)
                        FROM Spec_weaknesses
                        JOIN all_types ON Spec_weaknesses.attacker_type = all_types.type_id
                        GROUP BY type_name""", (pokemon.types,))
        pokemon_weaknesses = cursor.fetchall()
        result = dict()
        for type, mult_list in pokemon_weaknesses:
            mult = math.prod(mult_list)
            if mult >= 2:
                result[type] = int(mult)
        pokemon.weaknesses = result
        return pokemon
    
    
def insert_into_pokedex(user_id: int, pokemon_id: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""INSERT INTO pokedex (user_id, pokemon_id)
                       VALUES (%s, %s);""", (user_id, pokemon_id))
        
        print('Pokemon data has been added to the Pokedex successfuly!')
        
        
def get_from_pokedex(user_id: int) -> list:
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT pokemon_name, file_name FROM pokemon_basic_info
                    JOIN pokedex ON pokedex.pokemon_id = pokemon_basic_info.pokemon_id
                    WHERE user_id = %s;""", (user_id, ))
        
        pokemon = cursor.fetchall()
        return pokemon
    
    
def check_in_pokedex(user_id: int, pokemon_id: str) -> datetime:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT pokemon_caught FROM pokedex WHERE user_id = %s AND pokemon_id = %s;", (user_id, pokemon_id))
        caught_at = cursor.fetchone()
        
        if caught_at:
            caught_at = datetime.strftime(caught_at[0], "%d.%m.%Y")
            return caught_at
        return None
        
        