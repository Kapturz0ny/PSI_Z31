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
        temp_id = bstream.read(4)
        id = struct.unpack("!I", temp_id)[0]

        temp_charlen = bstream.read(2)
        charlen = struct.unpack("!H", temp_charlen)[0]

        string = bstream.read(charlen).__str__()

        return Element(id, charlen, string)



class Node:
    def __init__(self, elem: Element, next_node: 'Node' = None):
        self.elem = elem
        self.next_node = next_node


class LinkedList:
    def __init__(self):
        self.head = None
    


def deserialize(bstream: io.BytesIO) -> LinkedList:
    while True:
        e = Element.from_bstream(bstream)
        print(e)

        