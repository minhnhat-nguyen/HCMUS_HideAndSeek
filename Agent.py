from abc import abstractmethod
from pathfinder import position
from pathfinder import get_possible_moves
import uuid


class Agent:
    def __init__(self, x: int, y: int) -> None:
        self.id = uuid.uuid4()
        self._position = position(x, y)
        self.point = 100

    @abstractmethod
    def move(self, step: int) -> None:
        pass

    def _get_posible_moves(self) -> list[position]:
        x = self._position.x
        y = self._position.y
        return get_possible_moves(x, y)

    def getPosition(self) -> position:
        return self._position
