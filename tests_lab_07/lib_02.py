from collections import Counter
from typing import Optional, Iterable, Sequence
from pathlib import Path
import re, csv, json
from openpyxl.utils import get_column_letter 
from openpyxl import Workbook

def min_max (nums: list[float | int]) -> tuple[float | int, float | int]:
    if len(nums) == 0: return ValueError
    return (min(nums), max(nums))

def unique_sorted (nums: list[float | int]) -> list[float | int]:
    return sorted(list(set(nums)))

def flatten(mat: list[list | tuple]) -> list:
    st = set()
    for i in mat:
        if type(i) == list or type(i) == tuple:
            for j in i:
                if type(j) == int or type(j) == float:
                    st.add(j)
                else: return TypeError
        else: return TypeError
    return list(st)

def check_rectangular(mat: list[list[float | int]]) -> bool:
    if not mat:
        return True
    row_len = len(mat[0])
    for row in mat:
        if len(row) != row_len:
            return False
    return True

def transpose(mat: list[list[float | int]]) -> list | ValueError:
    if not mat:
        return []
    if check_rectangular(mat):
        return [list(col) for col in zip(*mat)]
    return ValueError("Матрица рваная (строки разной длины)")

def row_sums(mat: list[list[float | int]]) -> list[int] | list[float] | ValueError:
    if not mat:
        return []
    if check_rectangular(mat):
        return [sum(row) for row in mat]
    return ValueError("Матрица рваная (строки разной длины)")

def col_sums(mat: list[list[float | int]]) -> list[int] | list[float] | ValueError:
    if not mat:
        return []
    if check_rectangular(mat):
        return [sum(col) for col in zip(*mat)]
    return ValueError("Матрица рваная (строки разной длины)")

def format_record(rec: tuple[str, str, float]) -> str:

    if not isinstance(rec, tuple) or len(rec) != 3:
        raise TypeError("rec должен быть кортежем из 3 элементов (ФИО, группа, GPA)")
    if not isinstance(rec[0], str):
        raise TypeError("ФИО должно быть строкой")
    if not isinstance(rec[1], str):
        raise TypeError("Группа должна быть строкой")
    if not isinstance(rec[2], (int, float)):
        raise TypeError("GPA должно быть числом int или float")

    s = rec[0].split()
    
    if len(s) == 3:
        return f'{s[0].capitalize()} {s[1][0].upper()}.{s[2][0].upper()}., гр. {rec[1]}, GPA {rec[2]:.2f}'
    elif len(s) == 2:
        return f'{s[0].capitalize()} {s[1][0].upper()}., гр. {rec[1]}, GPA {rec[2]:.2f}'
    else:
        raise ValueError('Неверный формат ФИО')
    
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if yo2e == True:
        text = text.replace('Ё','Е').replace('ё','е')
    if casefold == True:
        text = text.casefold()
    for spaces in ['\t', '\r', '\n']:
        text = text.replace(spaces,' ')
    words = text.split()
    text = ' '.join(words)
    return text

def tokenize(text: str) -> list[str]:
    simv = r'\b[а-яёa-zA-Z0-9_]+(?:-[а-яёa-zA-Z0-9_]+)*\b'
    return re.findall(simv,text)

def count_freq(tokens: list[str], top_n: Optional[int] = None) -> dict[str, int]:
    counter = Counter(tokens)
    if top_n is not None:
        return dict(counter.most_common(top_n))
    return dict(counter)

def table(text: str, n: int = 5):
    print(f'Всего слов: {len(tokenize(normalize(text)))}')
    print(f'Уникальных слов: {len(set(tokenize(normalize(text))))}')
    print('Топ-5:')
    text = count_freq(tokenize(normalize(text)))
    item = dict(list(text.items())[:n])
    for keys, values in item.items():
        print(f"{keys}: {values}")
    print ('')
    print("слово        | частота")
    print("----------------------")
    for keys, values in item.items():
        print(f"{keys:<12} | {values}")

def write_csv(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    p = Path(path)
    
    # Проверка расширения файла
    if p.suffix.lower() != ".csv":
        raise ValueError("Неверный формат файла: ожидается .csv")
    
    # Преобразуем в список чтобы можно было несколько раз использовать
    rows = list(rows)
    
    # Проверка что все строки одинаковой длины
    if rows:  # проверяем только если есть строки
        first_row_length = len(rows[0])
        for i in range(1, len(rows)):
            if len(rows[i]) != first_row_length:
                raise ValueError("Все строки должны иметь одинаковое количество колонок")
    
    # Запись в файл
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        if header is not None:
            # УБЕРИ ЭТУ ПРОВЕРКУ - она вызывает проблему!
            # if rows and len(header) != len(rows[0]):
            #     raise ValueError("Количество колонок в заголовке не соответствует данным")
            writer.writerow(header)
        writer.writerows(rows)  # записываем все строки за один раз

def write_any_text(rows: Iterable[Sequence], path: str | Path,
              header: tuple[str, ...] | None = None) -> None:
    p = Path(path)
    rows = list(rows)
    for index in range(1, len(rows)):
        if len(rows[index-1]) != len(rows[index]):
            return ValueError
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if header is not None:
            if len(header) == len(rows[0]):
                w.writerow(header)
            else:
                return "Ошибка"
        for r in rows:
            w.writerow(r)

def read_text (path : str|Path , encoding: str = 'utf-8-sig') -> str:
    p = Path(path)
    try:
        return p.read_text(encoding=encoding)
    except FileNotFoundError:
        return 'Файл не найден'
    except UnicodeDecodeError:
        return 'Ошибка кодировки'
    
    
def json_to_csv(json_path: str, csv_path: str) -> None:
    
    json_file = Path(json_path)
    # Проверка на правильность файла
    if not json_file.exists ():
        raise FileNotFoundError('Файл не найден')
    
    if json_file.suffix.lower() != '.json':
        raise ValueError('Неверный тип файла, ожидается .json')
    
    with open(json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # фиксса JSON
    content = content.replace('﻿', '')  # убираем BOM
    content = content.replace('" "', '"')  # убираем пробелы в ключах
    content = content.replace('}\n\n  {', '},\n  {')  # добавляем запятые между объектами
    
    # Делаем валидный JSON
    if not content.strip().startswith('['):
        content = '[' + content + ']'
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError ('Ошибка декодирования JSON')
   
    if not data:
        raise ValueError('Файл пустой')
    

    data_mas = []
    
    if isinstance(data, list) and all(isinstance(item,dict) for item in data):
        data_mas = data
    
    elif isinstance (data, dict):
        data_mas = [data]
    
    elif isinstance(data, list):
        data_mas = [{"value": item} for item in data]
    
    else:
        raise ValueError('json должен быть словарем или списком словарей')
    
    # Формирование заголовков
    if data_mas:
        first_lines = list(data_mas[0].keys())
        all_lines = set (first_lines)
        
        for item in data_mas[1:]:
            all_lines.update(item.keys())
        another_lines = sorted ( all_lines - set(first_lines) )
        final_lines = first_lines + another_lines
    else:
        final_lines = []
    rows= []
    for item in data_mas:
        row = [item.get(val,' ') for val in final_lines]
        rows.append(row)
    try:
        write_csv(rows, csv_path, header = tuple(final_lines))
        print ('Работа выполнена')
    except Exception as e:
        raise ValueError (f'Ошибка записи CSV')
    
# print (json_to_csv('data/asd.json', 'data/qwe.csv'))


def csv_to_json(csv_path: str, json_path: str):
    csv_file = Path(csv_path)
    
    # Проверка
    if not csv_file.exists():
        raise FileNotFoundError('Файл не найден')
    
    if csv_file.suffix.lower() != '.csv':
        raise ValueError('Неверный тип файла, ожидается .csv')
    
    try:
        # ✅ ПРАВИЛЬНО: читаем CSV один раз с правильной кодировкой
        with open(csv_file, 'r', encoding='utf-8-sig') as f:  
            reader = csv.DictReader(f)
            
            if reader.fieldnames is None:
                raise ValueError('CSV не содержит заголовки')
            
            data = list(reader)
            
    except UnicodeDecodeError as e:
        raise ValueError('Ошибка кодировки CSV')
    except csv.Error as e:
        raise ValueError('Ошибка синтаксиса CSV')
    
    if not data:
        raise ValueError('CSV файл пустой (только заголовки)')
    
    
    with open(json_path, 'w', encoding='utf-8') as f:  #
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print('Выполнено успешно')
    
# print (csv_to_json('data/qwe.csv','data/asd.json'))


def csv_to_xlsx(csv_path: str | Path, xlsx_path: str | Path) -> None:
    csv_path, xlsx_path = Path(csv_path), Path(xlsx_path)
    
    # Проверка
    if not csv_path.exists():
        raise FileNotFoundError('Файл не найден')
    if csv_path.suffix.lower() != '.csv':
        raise ValueError('Неверный тип файла, ожидактся .csv')
    try:
        with open (csv_path, 'r', encoding = 'utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
    except UnicodeDecodeError:
        raise ValueError ('Ошибка кодировки')
    except csv.Error:
        raise ValueError ('Ошибка формата CVS')
    if not data:
        raise ValueError ('Файл пустой')
    
    # Создание excel файла
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet_1"
    
    # Чтение csv и запись в excel
    with csv_path.open(encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            ws.append(row)
    
    wb.save(xlsx_path)
    return "Выполнено успешно"

# print (csv_to_xlsx('data/qwe.csv', 'data/ex.xlsx'))

    
    