import random
from pathfinder import position
from Agent import Agent
import GameMaster
import uuid

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

    def announcePos(self) -> tuple[uuid.UUID, position | None]:
        return (self.id, 
            None if self.__isFound else
            random.choices(
                [
                    (self._position + position(x, y)) 
                    for x in range(-2, 3) 
                    for y in range(-2, 3)
                    if (0 <= self._position.x + x < len(GameMaster.GameMaster.hidden_map)) and 
                    (0 <= self._position.y + y < len(GameMaster.GameMaster.hidden_map[0])) and 
                    (GameMaster.GameMaster.hidden_map[self._position.x + x][self._position.y + y] == 0)
                ],
                k=1
            )[0]
        )
