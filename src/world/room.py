from typing import Self

import pygame

DELIM = "\\xC0"
TILE_SIZE = (50, 50)

class Tile():
    def __init__(self):
        self.char = 'a'

class Room():
    def __init__(self, size: tuple[int, int], arr:bytearray | None, encoding: dict[int, Tile]): 
        self.width = size[0]
        self.height = size[1]
        if arr:
            self.arr = arr
        else:
            self.arr = bytearray(size[0] * size[1])

    def set_tile(self, pos: tuple[int, int], t: Tile):
        self.arr[pos[0] + pos[1]*self.width]

    def get_tile_raw(self, pos: tuple[int, int]) -> int:
        return self.arr[pos[0] + pos[1]*self.width]

    def get_tile(self, pos: tuple[int, int]) -> Tile:
        return self.encoding[self.arr[pos[0] + pos[1]*self.width]]

    def debug(self):
        for i in range(0, self.height):
            print(self.arr[i*self.width:(i+1)*self.width])

    def draw(self, screen, camera):
        x, y = pos
        # if x to the left of the left screen border,
        #   xstart = get how many tiles it is left by (floored)
        #   if xstart > self.width, return
        # if x + width is to the right of the right screen border
        pass

    def update(self):
        pass
        
    @staticmethod
    def from_str(txt: str) -> Self:
        r = txt.split(DELIM)
        return Room((int(r[0]), int(r[1])), bytearray(r[2], 'utf-8'), None)
 
    @staticmethod
    def to_str(room: Self) -> str:
        return str(room.width) + DELIM + str(room.height) + DELIM + room.arr.decode('utf-8')
    
def test():
    a = "5"+DELIM+"5"+DELIM+"AAAAB"+"AAAAB"+"AABBB"+"BAAAB"+"BBBBB"
    b:Room = Room.from_str(a)
    b.debug()
    c = Room.to_str(b)

    print(c)
    print(c == a)
test()