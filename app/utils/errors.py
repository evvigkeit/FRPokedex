from enum import Enum


class RegError(str, Enum):
    
    # AUTHORIZATION ERRORS
    
    WRONG_PASSWORD = "Oops, wrong password!"
    INVALID_USER = "Oops, that user doesn't exist!"
    
    # REGISTRATION DB ERRORS
    
    USERNAME_TAKEN = "Oops, that username is already taken!"
    EMAIL_TAKEN = "A user with that email already exists!"
    PHONE_TAKEN = "A user with that phone already exists!"
    
    # REGISTRATION DATA FORMAT ERRORS
    
    PHONE_FORMAT = "The phone number doesn't match the required format!"
    PASSWORD_MISMATCH = "The passwords don't match! Let's try again!"
    PASSWORD_NO_DIGIT = "Password must contain a digit!"
    PASSWORD_NO_LOWERCASE = "Password must contain a lowercase latin letter!"
    PASSWORD_NO_UPPERCASE = "Password must contain an uppercase latin letter!"
    PASSWORD_NO_SYMBOL = "Password must contain a special symbol!"
    PASSWORD_UNKNOWN_SYMBOL = "Password can contain only digits, latin letters and special symbols!"
    
    
    
