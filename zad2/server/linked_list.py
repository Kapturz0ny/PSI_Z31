import io
import struct

class Element:
    def __init__(self, id: int, charlen: int, string: str):
        self.id = id
        self.charlen = charlen
        self.string = string
    
    def __str__(self):
        return f'id:{self.id:05}, len:{self.charlen:02} : {self.string}'
    
    @classmethod
    def from_bstream(cls, bstream: io.BytesIO):
        net_id = bstream.read(4)
        net_charlen = bstream.read(2)

        try:
            id = struct.unpack("!I", net_id)[0]
            charlen = struct.unpack("!H", net_charlen)[0]
        except struct.error:
            # end of stream
            return None

        string = bstream.read(charlen).__str__()

        return Element(id, charlen, string)



class Node:
    def __init__(self, elem: Element, next_node: 'Node' = None):
        self.elem = elem
        self.next_node = next_node


class LinkedList:
    def __init__(self, head: Node = None):
        self.head = head
        self.tail = head
        self.size = 0 if head is None else 1
    
    def add(self, elem: Element):
        node = Node(elem)
        if self.head is None:
            self.head = node
            self.tail = node
        elif self.head == self.tail:
            self.head.next_node = node
            self.tail = node
        else:
            self.tail.next_node = node
            self.tail = self.tail.next_node
        self.size += 1
    
    def print(self):
        node = self.head
        while node is not None:
            print(node.elem)
            node = node.next_node
    


def deserialize(bstream: io.BytesIO) -> LinkedList:
    l_list = LinkedList()
    while True:
        e = Element.from_bstream(bstream)
        if e is None:
            break
        l_list.add(e)
    return l_list


        