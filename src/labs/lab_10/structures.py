
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
    
    
