from pydantic import BaseModel, Field, field_validator, model_validator
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
            raise ValueError('The phone number does not match the required format')
        return phone
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, password: str):
        special_symbols = "\\!#$%&'()*+,-./:;<=>?@[^_`{|}~]\""
        error_dict = {"digit": ["Password must contain a digit!", 0], 
                      "letter": ["Password must contain a latin letter!", 0], 
                      "uppercase": ["Password must contain an uppercase letter!", 0], 
                      "symbol": ["Password must contain a special symbol!", 0]}
       
        for element in password:
            if element.isdigit():
                error_dict["digit"][1] += 1
            elif 90 >= ord(element) >= 65:
                error_dict["uppercase"][1] += 1
            elif 122 >= ord(element) >= 97:
                error_dict["letter"][1] += 1
            elif element in special_symbols:
                error_dict["symbol"][1] += 1
            else:
                raise ValueError("Password can contain only digits, latin letters and special symbols!")
            
        print(ord("A"), ord("Z"), ord("a"), ord("z"))
            
        for value in error_dict.values():
            if value[1] == 0:
                raise ValueError(value[0])
        
        return password
    
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.ch_password:
            raise ValueError("The passwords don't match!")
        return self
        