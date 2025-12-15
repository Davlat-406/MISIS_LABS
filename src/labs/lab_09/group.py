import csv
from pathlib import Path
from lab_08.models import Student 

class Group:
    def __init__(self, path):
        self.path = Path(path)
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        if not self.path.exists():
            with open(self.path, 'w', newline='', encoding='utf-8-sig') as f:
                f.write('fio,birthdate,group,gpa\n')
        else:
            with open(self.path, 'r', encoding='utf-8-sig') as f:
                first_line = f.readline().strip()
                if first_line != 'fio,birthdate,group,gpa':
                    raise ValueError('Отсутствует или некорректен заголовок CSV файла')
    
    def list(self):
        students = []
        with open(self.path, 'r', encoding='utf-8-sig') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  
            for row in csv_reader:
                
                student_dict = {
                    'fio': row[0],
                    'birthdate': row[1],
                    'group': row[2],
                    'gpa': float(row[3]) 
                }
                students.append(Student.from_dict(student_dict))
        return students
    
    def add_student(self, student: Student):
        with open(self.path, 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['fio', 'birthdate', 'group', 'gpa'])
            writer.writerow(student.to_dict())
    
    def find(self, substring: str):
        with open(self.path, 'r', encoding='utf-8-sig') as f:
            rows = list(csv.DictReader(f))
        return [Student.from_dict(row) for row in rows if substring in row['fio']]
    
    def remove(self, st_name: str):

        all_st = self.list() 
        remove_st = [s for s in all_st if s.fio != st_name]
        
        with open(self.path, 'w', newline='', encoding='utf-8-sig') as f:
            f.write('fio,birthdate,group,gpa\n')
            for student in remove_st:
                f.write(f'{student.fio},{student.birthdate},{student.group},{student.gpa}\n')
    
    def update(self, st_name, **fields):
        with open(self.path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        found = False
        for row in rows:
            if row['fio'] == st_name:
                for key, value in fields.items():
                    if key in ['birthdate', 'group', 'gpa']:
                        row[key] = value
                found = True
                break
        if found:
            with open(self.path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['fio', 'birthdate', 'group', 'gpa'])
                writer.writeheader()
                writer.writerows(rows)
        return found

