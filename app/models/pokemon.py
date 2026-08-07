from dataclasses import dataclass
from app.utils.pokemon_util import TypeColor

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
    
    '''
    @property
    def types_div(self):
        types_dict = dict()
        
        for el in self.types:
            types_dict[TypeColor[el].name] = TypeColor[el].value
        return types_dict
    '''
    
    @staticmethod
    def property_color(type):
        return TypeColor[type].value