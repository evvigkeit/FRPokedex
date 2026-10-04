from dataclasses import dataclass
from enum import Enum


@dataclass
class Pokemon:
    id: int
    name: str
    description: str = None
    height: str = None
    weight: str = None
    gender_id: str = None
    category: str = None
    pic: str = None
    types: tuple = None
    weaknesses: dict = None
    
    @property
    def gender(self):
        all_genders = {0: 'Unknown', 1: 'W', 2: 'M', 3: 'W/M'}
        return all_genders[self.gender_id]
    
    @staticmethod
    def property_color(type):
        return TypeColor[type].value
    

class TypeColor(Enum):
    Normal = '#acaba9'
    Fighting = '#e75548'
    Poison = '#dd5fca'
    Ground = '#c58324'
    Flying = '#92a6d8'
    Bug = '#83aa35'
    Rock = '#c5a991'
    Ghost = '#6d83b4'
    Steel = '#d9d9d9'
    Fire = '#f3ab49'
    Water = '#56aeed'
    Grass = '#a2d063'
    Electric = '#fbfd5c'
    Ice = '#bbe9f8'
    Psychic = '#d4756f'
    Dragon = '#2f6ebe'
    Dark = '#6934a0'