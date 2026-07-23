from enum import Enum


class RegError(str, Enum):
    
    # AUTHORIZATION ERRORS
    
    WRONG_PASSWORD = "Oops, wrong password!"
    INVALID_USER = "Oops, that user doesn't exist!"
    
    # REGISTRATION ERRORS
    
    USERNAME_TAKEN = "Oops, that username is already taken!"
    EMAIL_TAKEN = "A user with that email already exists!"
    PHONE_TAKEN = "A user with that phone already exists!"
    PASSWORD_MISMATCH = "The passwords don't match! Let's try again!"
