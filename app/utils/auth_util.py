import os

from app.models.user import User
from app.models.pydantic_models import ApiResponse
from app import db
from app.utils.errors import RegError
from app.utils.security_util import verify_password


def validate_auth(user: User):
    user_from_db = db.check_user_exist(user)
    if user_from_db:
        if not verify_password(user.password, user_from_db.password):
            return ApiResponse(success=False, error=RegError.WRONG_PASSWORD)
        return ApiResponse()
    verify_password(user.password, os.getenv("FAKE_PASSWORD"))   # the timing attack prevention
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
