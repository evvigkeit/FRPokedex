import psycopg2
import os
from dotenv import load_dotenv
from app.models.user import User

load_dotenv()  # get secret data from .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(dbname="FRPokedex", host="localhost", user=DB_USER, password=DB_PASSWORD, port="5432")
print(("this shiii failed :(", 'ok!')[bool(conn)])

cursor = conn.cursor()

def check_user_exist(user: User):
    cursor.execute("""SELECT user_name, user_email, user_phone, user_created, user_password 
                       FROM user_data 
                       WHERE user_name=%s OR user_email=%s OR user_phone=%s""", (user.username, user.email, user.phone))
    user_from_db = cursor.fetchone()
    if user_from_db:
        return User(*user_from_db)
    return None

def get_user_data(username: str): # TEMPORARY LOGIC TILL I ADD SESSIONS 
    cursor.execute("SELECT user_name, user_email, user_phone, user_created FROM user_data WHERE user_name=%s", (username,))
    user_from_db = cursor.fetchone()
    if user_from_db:
        return User(*user_from_db)
    return None

def create_user(new_user: User):
    print(new_user)
    cursor.execute("""INSERT INTO user_data (user_name, user_email, user_phone, user_password) 
                   VALUES (%s, %s, %s, %s)""", (new_user.username, new_user.email, new_user.phone, new_user.password))
    conn.commit()
    print('User data has been added successfuly!')


