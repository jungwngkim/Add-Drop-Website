# Simple wrapper class for student info
class Student:
    def __init__(self, email: str, name: str, grade: int) -> None:
        self.email = email
        self.name = name
        self.grade = grade

    def __str__(self) -> str:
        return f"Student({self.email}, {self.name}, {self.grade})"
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.email == other.email and self.name == other.name and self.grade == other.grade
