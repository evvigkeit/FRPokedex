from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    username: str
    email: str = None
    phone: str = None
    created: str = None
    password: str = None
    
    @property
    def days_with_us(self):
        return(datetime.now() - self.created).days

    