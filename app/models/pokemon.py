from dataclasses import dataclass

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
    
    @property
    def gender(self):
        all_genders = {0: 'Unknown', 1: 'W', 2: 'M', 3: 'W/M'}
        return all_genders[self.gender_id]
    