from abc import abstractmethod
from pathfinder import position
from pathfinder import get_possible_moves

class Agent:
    def __init__(self, x: int, y: int) -> None:
        self._position : position = position(x, y)
        self.point = 100
        self.path = []
        
    @abstractmethod
    def move(self) -> position:
        pass

    def _get_posible_moves(self) -> list[position]:
        x = self._position.x
        y = self._position.y
        return get_possible_moves(x, y)

    def getPosition(self) -> position:
        return self._position