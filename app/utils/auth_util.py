from app.models.user import User
from app import db
from app.utils.errors import RegError


def validate_auth(user: User):
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        if user.password != user_from_db.password:
            return {"success": False, "error": RegError.WRONG_PASSWORD}
        return {"success": True, "error": None}
    return {"success": False, "error": RegError.INVALID_USER}
    
    
def validate_reg(user: User, ch_password: str): 
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        if user.username == user_from_db.username:
            return {"success": False, "error": RegError.USERNAME_TAKEN}
        elif user.phone == user_from_db.phone:
            return {"success": False, "error": RegError.PHONE_TAKEN}
        elif user.email == user_from_db.email:
            return {"success": False, "error": RegError.EMAIL_TAKEN}
    if user.password  != ch_password:
        return {"success": False, "error": RegError.PASSWORD_MISMATCH}
    return {"success": True, "error": None}
