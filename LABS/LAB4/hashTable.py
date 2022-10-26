# used chaining to avoid the collision 

import numpy as np

class Node: 
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self):
        self.capacity = 50
        self.size = 0
        self.ele = [None]*50
        self.elements1 = [self.ele]*50
        self.elements = np.array(self.elements1)

    def hash(self, key):
        hashsum = 0
        for i in key:
            hashsum += ord(i)*93
            hashsum = hashsum % self.capacity
        
        return hashsum
        
    def double_hash(self, key):
        hashsum = 0

        for i in key:
            hashsum += ord(i)*31
            hashsum = hashsum % self.capacity
        
        return hashsum

    def insert(self, key, value):
        self.size += 1
        inx = self.hash(key)
        i = self.double_hash(key)

        if (self.elements[inx][i] is None):
            self.elements[inx][i] = Node(key, value)
            return True
        return False

    def find(self, key):
        inx = self.hash(key)

        for i in self.elements[inx]:
            if (i is not None):
                if(key == i.key):
                    return True
        return False

    def get_value(self, key):
        inx = self.hash(key)

        for i in self.elements[inx]:
            if (i is not None):
                if(key == i.key):
                    return i.value
        return 0
    

    def delete(self, key):
        inx = self.hash(key)
        nn = None
        result = None

        for node in self.elements[inx]:
            nn = node.next
            if (nn is None):
                return None
            if(nn.key ==  key):
                self.sz -= 1
                result = nn.value
                node.next = nn.next
                break
        
        return result
                


    def get_nodes(self):
        arr = []
        for inx in self.elements:
            for i in inx: 
                if(i is not None):
                    arr.append(i.key)
                    arr.append(i.value)
        return arr
