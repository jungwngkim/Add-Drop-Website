# Simple wrapper class for student info
import random
from . import globals

class Student:
    def __init__(self, email: str, name: str, grade: int) -> None:
        self.email = email
        self.name = name
        self.grade = grade
        
        # create unique register number
        register_id = random.randint(0, 999)
        while register_id in globals.register_id_set:
            register_id = random.randint(0, 999)
        globals.register_id_set.add(register_id)
        self.register_id = register_id


    def __str__(self) -> str:
        return f"Student({self.email}, {self.name}, {self.grade})"
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.email == other.email and self.name == other.name and self.grade == other.grade
