import random
from pathfinder import position
from Agent import Agent

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.hiderLastPos = position(0, 0)
    def move(self, map : list[list[int]]) -> position:
        self.position = random.choice(self._get_posible_moves(map))
        return self.position