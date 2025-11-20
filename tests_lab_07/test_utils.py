import pytest
import json
import csv
from pathlib import Path
from labs.lab_07.lib_02 import *
Normailize_Test = [
        ("ПрИвЕт \nМИр\t", "привет мир"),
        ("ёжик, Ёлка", "ежик, елка"),
        ("Hello\r\nWorld", "hello world"),
        ("  двойные   пробелы  ", "двойные пробелы"),
    ]
Tokenize_Test = [
        ("привет, мир!", ["привет", "мир"]),
        ("hello world", ["hello", "world"]),
        ("test-test", ["test-test"]),
    ]
Test_count_freq_and_top_n = [
    (["a","b","a","c","b","a"],None,{'a': 3, 'b': 2, 'c': 1}),
    (["a","b","a","c","b","a"],2,{'a': 3, 'b': 2}),# C top_n
    (["bb","aa","bb","aa","cc"],1,{'bb': 2})# С top_n   
]

@pytest.mark.parametrize("source, expected",Normailize_Test)
def test_normalize(source, expected):
   assert normalize(source) == expected
    
@pytest.mark.parametrize("source, expected",Tokenize_Test)

def test_tokenize(source, expected):
    assert tokenize(source) == expected

@pytest.mark.parametrize("source, top_n, expected",Test_count_freq_and_top_n)

def test_count_freq_and_top_n(source,top_n, expected):
    assert count_freq(source, top_n) == expected


def test_json_to_csv(tmp_path: Path):
    folder_dir = tmp_path / "root_folder"
    folder_dir.mkdir(parents=True, exist_ok=True)
    json_path = tmp_path / 'root_folder/asd.json'
    csv_path = tmp_path / 'root_folder/qwe.csv'
    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    json_to_csv(str(json_path), str(csv_path))
    
    with csv_path.open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    
    cleaned_rows = []
    for row in rows:
        cleaned_row = {}
        for key, value in row.items():
            cleaned_key = key.lstrip('\ufeff')  
            cleaned_row[cleaned_key] = value
        cleaned_rows.append(cleaned_row)  

    rows = cleaned_rows
    
    print(f"Количество строк после очистки: {len(rows)}")
    for i, row in enumerate(rows):
        print(f"Строка {i}: {row}")
    
    assert len(rows) == 2
    assert {'name', 'age'} <= set(rows[0].keys())

def test_csv_to_json(tmp_path:Path):
    folder_dir = tmp_path / "root_folder"
    folder_dir.mkdir(parents=True, exist_ok=True)
    csv_path = tmp_path / 'root_folder/qwe.csv'
    json_path = tmp_path / 'root_folder/asd.json'
    data = [
        {"name":"Alice", "age": 22},
        {"name":"Bob", "age": 25}
    ]
    with csv_path.open ('w',newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'age'])
        writer.writeheader()
        writer.writerows(data)
    csv_to_json(str(csv_path), str(json_path))
    
    with json_path.open(encoding='utf-8') as f:
        result = json.load(f)
        # Проверка заголовков
        assert len (result) == 2
        assert {'name', 'age'} <= set(result[0].keys())
        # Проверка значений
        assert result[0]['name'] == 'Alice'
        assert result[0]['age'] == '22'
        assert result[1]['name'] == 'Bob'
        assert result[1]['age'] == '25'