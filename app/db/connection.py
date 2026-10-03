import os
import psycopg2

from contextlib import contextmanager
from dotenv import load_dotenv


load_dotenv()  # get secret data from .env

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


@contextmanager
def get_db_connection():
    conn = psycopg2.connect(dbname="FRPokedex", host="localhost", user=DB_USER, password=DB_PASSWORD, port="5432")
    try:
        yield conn
        print(("this shiii failed :(", 'ok!')[bool(conn)])
        
    finally:
        conn.close()
        
        
@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        
        except Exception:
            conn.rollback()
            
        finally:
            cursor.close()
