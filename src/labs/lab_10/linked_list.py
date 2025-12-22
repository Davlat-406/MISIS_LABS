from typing import Any, Optional, Iterator

class Node:
    def __init__(self, value: Any, next_node: Optional['Node'] = None):
        self.value = value
        self.next = next_node

    def __repr__(self):
        return f"Node({self.value})"

class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, value: Any):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node  # Исправлено: self.tail.next, а не self.next
            self.tail = new_node
        self.size += 1
    
    def prepend(self, value: Any):
        new_node = Node(value, self.head)
        self.head = new_node
        if self.tail is None:
            self.tail = new_node
        self.size += 1
    
    def insert(self, idx: int, value: Any):  # Исправлено имя: isert -> insert
        if idx < 0 or idx > self.size:
            raise IndexError('Индекс лежит вне диапазона')
        
        if idx == 0:
            self.prepend(value)
            return
        
        if idx == self.size:
            self.append(value)
            return  # Добавлен return
            
        current = self.head
        for _ in range(idx-1):  # Исправлено: добавлен range()
            current = current.next
            
        new_node = Node(value, current.next)
        current.next = new_node
        self.size += 1 
     
    def remove_at(self, idx: int) -> None:
        if idx < 0 or idx >= self.size:
            raise IndexError('Индекс лежит вне диапазона')
        
        if idx == 0:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        else:
            current = self.head
            for _ in range(idx-1):  # Исправлено: добавлен range()
                current = current.next
            current.next = current.next.next
            
            if current.next is None:
                self.tail = current
        self.size -= 1
        
    def remove(self, value: Any) -> bool:
        if self.head is None:
            return False

        if self.head.value == value:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
            self.size -= 1
            return True  # Исправлено: было False, должно быть True
       
        current = self.head
        
        while current.next and current.next.value != value:
            current = current.next
            
        if current.next is None:
            return False
        
        current.next = current.next.next
        if current.next is None:
            self.tail = current
        self.size -= 1
        return True
    
    def __iter__(self) -> Iterator[Any]:
        current = self.head
        while current:
            yield current.value
            current = current.next
        
    def __len__(self) -> int:
        return self.size
    
    def __repr__(self):
        values = list(self)
        return f"SinglyLinkedList({values})"


# Тестирование SinglyLinkedList
ll = SinglyLinkedList()
print("SinglyLinkedList тесты:")
print(f"1. Пустой список: {ll}, длина: {len(ll)}")

ll.append(10)
print(f"2. После append(10): {ll}, длина: {len(ll)}")
print(f"3. head: {ll.head}, tail: {ll.tail}")

ll.append(20)
print(f"4. После append(20): {ll}, длина: {len(ll)}")
print(f"5. head: {ll.head}, tail: {ll.tail}")

ll.append(30)
print(f"6. После append(30): {ll}, длина: {len(ll)}")
print(f"7. head: {ll.head}, tail: {ll.tail}")

ll.prepend(5)
print(f"8. После prepend(5): {ll}, длина: {len(ll)}")
print(f"9. head: {ll.head}, tail: {ll.tail}")

try:
    ll.insert(2, 15)  # Исправлено имя метода
    print(f"10. После insert(2, 15): {ll}, длина: {len(ll)}")
except Exception as e:
    print(f"10. Ошибка insert: {e}")

ll.remove_at(1)
print(f"11. После remove_at(1): {ll}, длина: {len(ll)}")

result = ll.remove(20)
print(f"12. remove(20): {result}, список: {ll}, длина: {len(ll)}")

result2 = ll.remove(99)
print(f"13. remove(99): {result2}, список: {ll}, длина: {len(ll)}")

print(f"14. Итерация по списку:")
for item in ll:
    print(f"    {item}")

print(f"15. list(ll): {list(ll)}")

try:
    ll.remove_at(10)
except IndexError as e:
    print(f"16. remove_at(10): {e}")

try:
    ll.insert(10, 100)
except IndexError as e:
    print(f"17. insert(10, 100): {e}")

ll2 = SinglyLinkedList()
print(f"18. Пустой список: {ll2}, длина: {len(ll2)}")
print(f"19. remove из пустого: {ll2.remove(10)}")