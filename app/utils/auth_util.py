from app.models.user import User
from app.models.pydantic_models import ApiResponse
from app import db
from app.utils.errors import RegError


def validate_auth(user: User):
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        if user.password != user_from_db.password:
            return ApiResponse(success=False, error=RegError.WRONG_PASSWORD)
        return ApiResponse()
    return ApiResponse(success=False, error=RegError.INVALID_USER)
    
    
def validate_reg(user: User): 
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        if user.username == user_from_db.username:
            return ApiResponse(success=False, error=RegError.USERNAME_TAKEN)
        elif user.phone == user_from_db.phone:
            return ApiResponse(success=False, error=RegError.PHONE_TAKEN)
        elif user.email == user_from_db.email:
            return ApiResponse(success=False, error=RegError.EMAIL_TAKEN)
    return ApiResponse()
