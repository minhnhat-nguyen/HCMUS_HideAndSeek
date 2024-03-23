from abc import abstractmethod
from pathfinder import position

class Agent:
    def __init__(self, x: int, y: int) -> None:
        self.position = position(x, y)
        self.point = 100
    @abstractmethod
    def move(self, map : list[list[int]]) -> position:
        pass

    def _get_posible_moves(self, map : list[list[int]]) -> list[position]:
        moves : list[position] = []
        x = self.position.x
        y = self.position.y
        n = len(map)
        m = len(map[0])
        if x - 1 >= 0 and map[x - 1][y] != 1:
            moves.append(position(x - 1, y))
        if x + 1 < n and map[x + 1][y] != 1:
            moves.append(position(x + 1, y))
        if y - 1 >= 0 and map[x][y - 1] != 1:
            moves.append(position(x, y - 1))
        if y + 1 < m and map[x][y + 1] != 1:
            moves.append((position(x, y + 1)))
        return moves