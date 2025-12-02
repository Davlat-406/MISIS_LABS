from dataclasses import dataclass
from datetime import datetime,date
@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float

# Проверка даты рождения и значения gpa
    def __post_init__(self):
        try:
            datetime.strptime(self.birthdate, "%d-%m-%Y")
        except:
            raise ValueError('Введите правильный формат даты рождения dd-mm-yyyy')
        if not (0 <= self.gpa <= 10):
            raise ValueError ('gpa должен быть между 0 и 10')   
        
    # Проверка сколько лет студенту
    def age(self) -> int:
        birth_date = datetime.strptime(self.birthdate, "%d-%m-%Y").date()
        today = date.today()
        age = today.year - birth_date.year
        
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        return age
    
    def to_dict (self) -> dict:
        return{ "fio": self.fio,
                "birthdate": self.birthdate,
                "group": self.group,
                "gpa": self.gpa }
    @classmethod
    def from_dict(cls, data: dict ):
        return cls(
            fio = data["fio"],
            birthdate = data["birthdate"],
            group = data["group"],
            gpa = data["gpa"]
        )

    def __str__ (self):
        return f"Студент: {self.fio}, группа: {self.group}, возраст: {self.age()} лет, средний балл: {self.gpa}"

