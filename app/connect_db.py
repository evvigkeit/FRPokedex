import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # get secret data from .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(dbname="habit_tracker", host="localhost", user=DB_USER, password=DB_PASSWORD, port="5432")

if conn:
    print('ok!')
else:
    print("this shiii failed :(")

cursor = conn.cursor()

def add_user_data(user, password):
    cursor.execute(f"INSERT INTO user_data (username, user_password) VALUES ('{user}', '{password}')")
    conn.commit()
    print('User data hass been added successfuly!')