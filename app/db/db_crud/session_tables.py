from app.db.connection import get_db_cursor
from app.models.user import Session, User
from app.utils.db_util import check_session_valid


def add_session_data(session_data: Session):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""
                        INSERT INTO session_data(user_id, session_id, login_at, expires)
                        VALUES (
                            (
                                SELECT user_data.user_id FROM user_data
                                WHERE user_name = %s
                            ), 
                            %s, 
                            %s, 
                            %s
                        )""", (session_data.user, session_data.session_id, session_data.login, session_data.expires))
        print('Session data has been added successfuly!')
    
    
def check_session_by_username(session_id: str, username: str) -> bool:
    with get_db_cursor() as cursor:
        cursor.execute("""SELECT * FROM session_data 
                    WHERE session_id = %s AND user_id = (SELECT user_id FROM user_data WHERE user_name = %s)""", (session_id, username))
        
        session_data = cursor.fetchone()
        if session_data:
            session_valid = check_session_valid(session_data[3])
            if not session_valid:
                delete_session_from_db(session_data[1])
                return False
            return True
        return False
    
    
def delete_session_from_db(session_id: str):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""DELETE FROM session_data WHERE session_id = %s""", (session_id, ))
        print('Session data has been deleted successfuly!')
    

def get_user_by_session_id_from_db(session_id: str) -> User:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("""SELECT user_name, user_email, user_phone, user_created FROM user_data
                            JOIN session_data ON user_data.user_id = session_data.user_id
                            WHERE session_id = %s""", (session_id, ))
        user_from_db = cursor.fetchone()
        if user_from_db:
            session_valid = check_session_by_username(session_id, user_from_db[0])
            if session_valid:
                return User(*user_from_db)
        return None