from typing import Any

class Node:
    def __init__(self, data: Any):
        self.data = data
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        self._len = 0
    
    def insert(self, index: int, value: Any) -> None:
        if index < 0 or index > self._len:
            raise IndexError
        
        new_node = Node(value)
        
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            prev = self.head
            for _ in range(index-1):
                prev = prev.next
            new_node.next = prev.next
            prev.next = new_node
        self._len += 1
    
    def delete(self, index: int) -> object:
        if self._len == 0:
            raise IndexError
        if index < 0 or index > self._len:
            raise IndexError
        
        if index == 0:
            removed_node = self.head
            self.head = self.head.next
        else:
            prev = self.head
            for _ in range(index-1):
                prev = prev.next
            removed_node = prev.next
            prev.next = prev.next.next
            
        self._len -= 1
        return removed_node
        
    def to_list(self) -> list:
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result
    
    def __len__(self) -> int:
        return self._len
        
class CircularList:
    def __init__(self):
        self.cursor = None
        self._len = 0
    
    def insert(self, value: Any) -> None:
        new_node = Node(value)
        
        # 1 2() 3(c)
        if self.cursor == None:
            new_node.next = new_node
            self.cursor = new_node
            self._len = 1
        else:
            new_node.next = self.cursor.next
            self.cursor.next = new_node
            self.cursor = new_node
            self._len += 1
            
    def delete(self, value: Any) -> bool:
        if self.cursor == None:
            return False

        if self._len == 1:
            if self.cursor.data == value:
                self.cursor = None
                self._len = 0
                return True
            else:
                return False
        else:
            # 1 2 3 4(c) 5 value 5
            prev = self.cursor # 4
            current = self.cursor.next # 5
            for _ in range(self._len):
                if current.data == value:
                    prev.next = current.next
                    if current is self.cursor:
                        self.cursor = prev
                    self._len -= 1
                    return True
                prev = current
                current = current.next
            return False
    
    def get_next(self) -> object | None:
        if self.cursor == None:
            return None
        self.cursor = self.cursor.next
        return self.cursor
    
    def search(self, value: Any) -> bool:
        if self.cursor == None:
            return False
        current = self.cursor
        for _ in range(self._len):
            if current.data == value:
                return True
            current = current.next
        return False
        
def main():
    try:
        # list = LinkedList()
        # print(len(list))
        # list.insert(0, 'A')
        # list.insert(1, 'B')
        # list.insert(1, 'C')
        # print(list.to_list())
        # removed_node = list.delete(1)
        # print(removed_node.data)
        # print(list.to_list())
        # print(len(list))
        
        cl = CircularList()

        cl.insert('A')
        cl.insert('B')
        cl.insert('C')
        cl.insert('A')
        cl.insert('B')
        cl.get_next()
        cl.get_next()
        cl.print_list()
        
        cl.delete('B')
        cl.print_list()

    except IndexError:
        print("IndexError")
    # except Exception:
        # print("Exception")

    
if __name__ == "__main__":
    main()