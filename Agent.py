from abc import abstractmethod
from pathfinder import position
from pathfinder import get_possible_moves

class Agent:
    def __init__(self, x: int, y: int) -> None:
        self.position = position(x, y)
        self.point = 100
        self.path = []
        
    @abstractmethod
    def move(self, map : list[list[int]]) -> position:
        pass

    def _get_posible_moves(self, map : list[list[int]]) -> list[position]:
        x = self.position.x
        y = self.position.y
        return get_possible_moves(map, x, y)