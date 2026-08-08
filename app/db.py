import psycopg2
import os
import math
from dotenv import load_dotenv
from app.models.user import User
from app.models.pokemon import Pokemon

load_dotenv()  # get secret data from .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(dbname="FRPokedex", host="localhost", user=DB_USER, password=DB_PASSWORD, port="5432")
print(("this shiii failed :(", 'ok!')[bool(conn)])

cursor = conn.cursor()

def check_user_exist(user: User):
    cursor.execute("""SELECT user_name, user_email, user_phone, user_created, user_password 
                       FROM user_data 
                       WHERE user_name=%s OR user_email=%s OR user_phone=%s;""", (user.username, user.email, user.phone))
    user_from_db = cursor.fetchone()
    if user_from_db:
        return User(*user_from_db)
    return None

def get_user_data(username: str): # TEMPORARY LOGIC TILL I ADD SESSIONS 
    cursor.execute("SELECT user_name, user_email, user_phone, user_created FROM user_data WHERE user_name=%s;", (username,))
    user_from_db = cursor.fetchone()
    if user_from_db:
        return User(*user_from_db)
    return None

def create_user(new_user: User):
    print(new_user)
    cursor.execute("""INSERT INTO user_data (user_name, user_email, user_phone, user_password) 
                   VALUES (%s, %s, %s, %s);""", (new_user.username, new_user.email, new_user.phone, new_user.password))
    conn.commit()
    print('User data has been added successfuly!')
    
    
def get_pokemons(pokemon_name: str, limit: str = '10') -> list:
    cursor.execute("""SELECT pokemon_name, file_name FROM pokemon_basic_info
                        WHERE pokemon_name ILIKE %s LIMIT %s;""", ('%' + pokemon_name + '%', limit))
    pokemons = cursor.fetchall()
    return pokemons

def get_pokemon_info(pokemon_name: str) -> list:
    cursor.execute("SELECT * FROM pokemon_basic_info WHERE pokemon_name = %s;", (pokemon_name,))
    pokemon_info = cursor.fetchall()
    return Pokemon(*pokemon_info[0])


def get_pokemon_types(pokemon: Pokemon) -> list:
    cursor.execute("""SELECT type_name FROM pokemon_types
                        JOIN all_types ON pokemon_types.type_id = all_types.type_id
                        JOIN pokemon_basic_info ON pokemon_basic_info.pokemon_id = pokemon_types.pokemon_id
                        WHERE pokemon_name = %s""", (pokemon.name,))
    pokemon_types = cursor.fetchall()
    pokemon.types = tuple(map(lambda x: x[0], pokemon_types))
    return pokemon

def get_pokemon_weaknesses(pokemon: Pokemon) -> list:
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
    print(pokemon_weaknesses)
    for type, mult_list in pokemon_weaknesses:
        mult = math.prod(mult_list)
        if mult >= 2:
            result[type] = int(mult)
    print(result)
    pokemon.weaknesses = result
    return pokemon
