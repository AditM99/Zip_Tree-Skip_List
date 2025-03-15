# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file.

from typing import TypeVar
import random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

class Node:
    def __init__(self, key: KeyType, val: ValType, rank: int) -> None:
        self.key = key
        self.val = val
        self.rank = rank
        self.left = None
        self.right  = None

class ZipTree:
    def __init__(self):
        self.root = None
        self.size = 0

    @staticmethod
    def get_random_rank() -> int:
        rank = 0
        while random.randint(0, 1) == 0:
            rank += 1
        return rank

    def insert(self, key: KeyType, val: ValType, rank: int = -1):
        if rank == -1:
            rank = self.get_random_rank()
        new_node = Node(key, val, rank)
    
        if self.root is None:
            self.root = new_node
            self.size += 1
            return

        parent, insert_ = self._insert(new_node)

        if insert_ is None:
            if parent.key > key:
                parent.left = new_node
            else:
                parent.right = new_node
            self.size += 1  # Increment size when a node is successfully inserted
            return

        if parent is None:
            p, q = self.unzip(new_node, insert_)
            new_node.left = p
            new_node.right = q
            self.root = new_node
        else:
            if parent.key < new_node.key:
                parent.right = new_node
            else:
                parent.left = new_node

            new_node.left, new_node.right = self.unzip(new_node, insert_)

        self.size += 1


    def _insert(self, node: Node) -> Node:
        insert_ = self.root
        parent = None

        while insert_ is not None:
            if insert_.rank < node.rank:
                return parent, insert_
            elif insert_.rank == node.rank and insert_.key > node.key:
                    return parent, insert_
            else:	
                parent = insert_		
                if insert_.key > node.key:
                    insert_ = insert_.left
                else:
                    insert_ = insert_.right
                    
        return parent, None
      
    def remove(self, key: KeyType):
        current = self.root
        while current:
            if key == current.key:
                break

            elif current.key < key:
                parent = current
                current = current.right
            else:
                parent = current
                current = current.left
        node = self.zip(current)
        if parent is None:
            self.root = node
            return
        elif parent.key > current.key:
            parent.left = node
        else:
            parent.right = node
        self.size -=1
        
    def find(self, key: KeyType) -> ValType:
        current = self.root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return current.val
        return None

    def get_size(self) -> int:
        return self.size

    def get_height(self) -> int:
        return self._get_height(self.root)

    def _get_height(self, node) -> int:
        if node is None:
            return -1
        return 1 + max(self._get_height(node.left), self._get_height(node.right))

    def get_depth(self, key: KeyType) -> int:
        depth = 0
        current = self.root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                return depth
            depth += 1
        return -1

    def zip(self, x: Node):
        def zip_up(p: Node, q: Node):
            if p is None: return q
            if q is None: return p
            if q.rank > p.rank:
                q.left = zip_up(p, q.left)
                return q
            else:
                p.right = zip_up(p.right, q)
                return p

        return zip_up(x.left, x.right)

    def unzip(self, x: Node, y: Node):
        def unzip_lookup(key: KeyType, node: Node):
            if node is None:
                return None, None
            elif node.key < key:
                p, q = unzip_lookup(key, node.right)
                node.right = p
                return node, q
            else:
                p, q = unzip_lookup(key, node.left)
                node.left = q
                return p, node
            
        return unzip_lookup(x.key, y)

# feel free to define new classes/methods in addition to the above
# fill in the definitions of each required member function (above),
# and any additional member functions you define
