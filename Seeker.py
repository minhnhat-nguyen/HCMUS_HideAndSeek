from pathfinder import a_star
from pathfinder import position
from Agent import Agent

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self._path = []
        self._latestTarget = position(0, 0)
        self.hiderLastPos : position | None = position(0, 0)
    def move(self, map : list[list[int]]) -> position:
        if self._latestTarget != self.hiderLastPos and self.hiderLastPos != None:
            self._path = a_star(map, self.position, self.hiderLastPos)
            self._latestTarget = self.hiderLastPos
        self.position = self._path[0]
        self._path = self._path[1:]
        return self.position