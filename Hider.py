from pathfinder import position, getChebyshev, getManhattan
from Agent import Agent
import GameMaster, uuid, random

class Hider(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__isFound = False
        self.__seekerLastPos : None | position = None 
        self.point = 20

    def move(self, step: int) -> None:
        seekerInRange = GameMaster.GameMaster.hiderGetSurrounding(self)
        moves = self._get_posible_moves()
        if seekerInRange is not None:
            self.__seekerLastPos = seekerInRange

        if self.__seekerLastPos is not None:
            pos = self._position
            for move in moves:
                nm = getChebyshev(move, self.__seekerLastPos)
                cm = getChebyshev(pos, self.__seekerLastPos)
                if nm > cm:
                    pos = move
                elif nm == cm:
                    if getManhattan(move, self.__seekerLastPos) >= getManhattan(pos, self.__seekerLastPos):
                        pos = move

            GameMaster.GameMaster.AgentMove(self, pos if pos else random.choice(moves))
        else:
            GameMaster.GameMaster.AgentMove(self, random.choice(moves))
                
            

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
