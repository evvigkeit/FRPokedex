from pydantic import BaseModel

class AuthForm(BaseModel):
    username: str
    password: str
    
    
class RegForm(BaseModel):
    username: str
    email: str
    phone: str
    password: str
    ch_password: str