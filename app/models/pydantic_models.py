from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_core import PydanticCustomError

from app.utils.errors import RegError
import re

class AuthForm(BaseModel):
    username: str
    password: str
    
    
class RegForm(BaseModel):
    username: str = Field(pattern=r"^[A-Za-z0-9_]+$")
    email: str = Field(pattern=r"^[A-Za-z]+[A-Za-z0-9]*@[A-Za-z]+\.[A-Za-z]+$")
    phone: str = Field(min_length=11, max_length=20)
    password: str = Field(min_length=8)
    ch_password: str
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, phone: str):
        pattern = re.compile(r"^(?:\+375|80)(\((?:29|44|33|25)\)|(?:29|44|33|25))([ -]?)[0-9]{3}\2[0-9]{2}\2[0-9]{2}$")
        
        if not pattern.search(phone):
            raise PydanticCustomError("phone_format", RegError.PHONE_FORMAT)
        return phone
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str):
        special_symbols = "\\!#$%&'()*+,-./:;<=>?@[^_`{|}~]\""
        error_dict = {"digit": ["password_no_digit", RegError.PASSWORD_NO_DIGIT, 0], 
                      "letter": ["password_no_lowercase", RegError.PASSWORD_NO_LOWERCASE, 0], 
                      "uppercase": ["password_no_uppercase", RegError.PASSWORD_NO_UPPERCASE, 0], 
                      "symbol": ["password_no_symbol", RegError.PASSWORD_NO_SYMBOL, 0]}
       
        for element in password:
            if element.isdigit():
                error_dict["digit"][2] += 1
            elif 90 >= ord(element) >= 65:
                error_dict["uppercase"][2] += 1
            elif 122 >= ord(element) >= 97:
                error_dict["letter"][2] += 1
            elif element in special_symbols:
                error_dict["symbol"][2] += 1
            else:
                raise PydanticCustomError("password_unknown_symbol", RegError.PASSWORD_UNKNOWN_SYMBOL)
            
        for err_type, err_mess, flag in error_dict.values():
            if flag == 0:
                raise PydanticCustomError(err_type, err_mess)
        
        return password
    
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.ch_password:
            raise PydanticCustomError("password_mismatch", RegError.PASSWORD_MISMATCH)
        return self
    

class ApiResponse(BaseModel):
    success : bool = True
    error: str | None = None
    