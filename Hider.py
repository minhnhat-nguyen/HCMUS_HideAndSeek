import random
from pathfinder import position
from Agent import Agent

class Hider(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__isFound = False

    def move(self) -> position:
        self._position = random.choice(self._get_posible_moves())
        return self._position
    
    def isFound(self) -> bool:
        return self.__isFound
    
    def markFound(self) -> None:
        self.__isFound = True

    def annoucePos(self) -> position:
        if self.__isFound:
            return position(-100000, -100000)
        return self._position