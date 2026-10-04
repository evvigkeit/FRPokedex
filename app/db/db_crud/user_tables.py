from app.db.connection import get_db_cursor
from app.models.user import User
from app.utils.security_util import get_password_hash


def check_user_exist(user: User):
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT user_name, user_email, user_phone, user_created, user_password, user_id 
                        FROM user_data 
                        WHERE user_name=%s OR user_email=%s OR user_phone=%s;""", (user.username, user.email, user.phone))
        user_from_db = cursor.fetchone()
        if user_from_db:
            return User(*user_from_db)
        return None


def create_user(new_user: User):
    with get_db_cursor(commit=True) as cursor:
        hashed_password = get_password_hash(new_user.password)
        cursor.execute("""INSERT INTO user_data (user_name, user_email, user_phone, user_password) 
                    VALUES (%s, %s, %s, %s);""", (new_user.username, new_user.email, new_user.phone, hashed_password))
        print('User data has been added successfuly!')
        