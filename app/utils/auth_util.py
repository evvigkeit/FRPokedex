from app.models.user import User
from app import db
from app.utils.errors import RegError


def validate_auth(user: User):
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        if user.password != user_from_db.password:
            return {"success": False, "error": RegError.WRONG_PASSWORD}
        return {"success": True, "error": None}
    return 2
    
    
def validate_reg(user: User): 
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        for i in ("username", "email", "phone"):
            if user.__getattribute__(i) == user_from_db.__getattribute__(i):
                return i
    return None
