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

