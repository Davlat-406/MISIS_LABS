import json
from pathlib import Path
import csv
import sys
sys.path.append(r"C:/Users/davla/OneDrive/Documents/GitHub/-_-/src")
from lib import *
from openpyxl import Workbook
from openpyxl.utils import get_column_letter 

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


def csv_to_json (csv_path: str, json_path: str):
    csv_file = Path(csv_path)
    
    # Проверка
    if not csv_file.exists ():
        raise FileNotFoundError('Файл не найден')
    
    if csv_file.suffix.lower() != '.csv':
        raise ValueError('Неверный тип файла, ожидается .csv')
    try:
        with open (csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if reader.fieldnames is None:
                raise ValueError ('CSV не содержит заголовки')
            data = list(reader)
    except UnicodeDecodeError as e:
            raise ValueError ('Ошибка кодировки CSV')
    except csv.Error as e:
            raise ('Ошибка синтаксиса CSV')
    if not data:
        raise ValueError('CSV файл пустой (только заголовки)')
    
    with open (csv_path, 'r', encoding = 'utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        json_file = {}
        for row in reader:
            json_file.update(row)

    with open (json_path,'w',newline = '', encoding = 'utf-8-sig') as f:
        json.dump(data, f, indent = 2, ensure_ascii = False)
        print ('Выполнено успешно')

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
