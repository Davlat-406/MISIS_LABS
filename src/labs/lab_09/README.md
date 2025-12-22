Реализован класс Group для работы с CSV
Основные методы:
### ```list()```
- получить всех студентов

```add(student)``` 
- добавить студента

```ind(substring)```
- поиск по подстроке

```remove(fio)```
- удалить по ФИО

```update(fio, **fields)``` 
- обновить данные

Формат CSV:
fio,birthdate,group,gpa
Иванов Иван Иванович,15-05-2000,БИВТ-21-1,4.5

Требования:
Кодировка UTF-8-sig

Формат даты: день-месяц-год (dd-mm-yyyy)

GPA: число от 0 до 10

GROUP
![](/misc/images/labs/lab_09/group_1.png)
![](/misc/images/labs/lab_09/group_2.png)

Result

![](/misc/images/labs/lab_09/group_terminal.png)

![](/misc/images/labs/lab_09/group_csv.png)
