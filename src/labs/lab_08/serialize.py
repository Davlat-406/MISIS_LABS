import json
from models import Student

def students_to_json(students, path):
    data = [s.to_dict() for s in students]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"Сохранено {len(students)} студентов в {path}"

def students_from_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        students = [Student.from_dict(item) for item in data]
        return students

    except FileNotFoundError: 
        print(f"Файл не найден")
        return []
    
    except json.JSONDecodeError: 
        print(f"Неправильный формат JSON в файле")
        return []
    
    except Exception as e: 
        print(f"Ошибка при загрузке студентов: {e}")
        return []


# Создание студентов для теста программы
student1 = Student(
    fio="Иванов Иван Иванович",
    birthdate="15-05-2000",
    group="Бивт-01",
    gpa=8.5
)

student2 = Student(
    fio="Фарту Масти Олегович",
    birthdate="22-08-2001",
    group="Бивт-02",
    gpa=9.0
)

print("=" * 50)
print("СОЗДАНИЕ СТУДЕНТОВ:")
print(f"1. {student1}")
print(f"2. {student2}")
    
# Сохраняем в json
print("\n" + "=" * 50)
print("СОХРАНЕНИЕ В JSON:")
result = students_to_json([student1, student2], "data/students.json")
print(result)
    
# Загрузка обратно
print("\n" + "=" * 50)
print("ЗАГРУЗКА ИЗ JSON:")
loaded_students = students_from_json("data/students.json")
    
if loaded_students:
    print(f"Успешно загружено {len(loaded_students)} студентов:")
    for i, student in enumerate(loaded_students, 1):
        print(f"{i}. {student}")
    else:
        print("Не удалось загрузить студентов")
    

    