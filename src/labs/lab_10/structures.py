
from collections import deque
from typing import Any, Optional

class Stack:
    
    def __init__(self) -> None:
        self._data = list()
        
    def _empty (self) -> bool:
        return len (self._data) == 0
    
    def push(self, item: Any ) -> None:
        self._data.append(item)
        
    def pop (self) -> Any:
        if self._empty():
            raise IndexError("Попытка pop из пустого стека")        
        else:
            return self._data.pop()
    
    def peek (self) -> Optional[Any]:
        if self._empty():
            return None
        return self._data[-1]

    def __len__ (self) -> int:
        return len (self._data)
    
    def __repr__(self):
        return f"Stack({self._data})"


class Queue:
    def __init__(self):
        self._data = deque()
        
    def _empty (self) -> bool:
        return len (self._data) == 0
    
    def enqueue (self, item: Any) -> None:
        self._data.append(item)
        
    def dequeue (self) -> Any:
        if self._empty():
            raise IndexError ('Попытка pop из пустой очереди')
        else:
            return self._data.popleft()
    
    def peek (self) -> Optional[Any]:
        if self._empty():
            return None
        else:
            return self._data[0]
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __repr__(self):
        return f"Queue({list(self._data)})" 
    
    
s = Stack()
print("Stack тесты:")
print(f"1. Пустой стек: {s}, длина: {len(s)}")
print(f"2. _empty пустого стека: {s._empty()}")

s.push(10)
print(f"3. После push(10): {s}, длина: {len(s)}")
print(f"4. peek: {s.peek()}")

s.push(20)
print(f"5. После push(20): {s}, длина: {len(s)}")
print(f"6. peek: {s.peek()}")

popped = s.pop()
print(f"7. pop: {popped}, стек после: {s}, длина: {len(s)}")

s.pop()
print(f"8. После второго pop: {s}, длина: {len(s)}")
print(f"9. _empty: {s._empty()}")

try:
    s.pop()
except IndexError as e:
    print(f"10. pop из пустого стека: {e}")

print("\n" + "="*50 + "\n")

# Тестирование Queue
q = Queue()
print("Queue тесты:")
print(f"1. Пустая очередь: {q}, длина: {len(q)}")
print(f"2. _empty пустой очереди: {q._empty()}")

q.enqueue("A")
print(f"3. После enqueue('A'): {q}, длина: {len(q)}")
print(f"4. peek: {q.peek()}")

q.enqueue("B")
print(f"5. После enqueue('B'): {q}, длина: {len(q)}")
print(f"6. peek: {q.peek()}")

dequeued = q.dequeue()
print(f"7. dequeue: {dequeued}, очередь после: {q}, длина: {len(q)}")
print(f"8. peek после dequeue: {q.peek()}")

q.dequeue()
print(f"9. После второго dequeue: {q}, длина: {len(q)}")
print(f"10. _empty: {q._empty()}")

try:
    q.dequeue()
except IndexError as e:
    print(f"11. dequeue из пустой очереди: {e}")

q.enqueue("C")
q.enqueue("D")
print(f"12. После добавления C и D: {q}, длина: {len(q)}")
print(f"13. peek: {q.peek()}")

first = q.dequeue()
second = q.dequeue()
print(f"14. Два dequeue: {first}, {second}, очередь: {q}")