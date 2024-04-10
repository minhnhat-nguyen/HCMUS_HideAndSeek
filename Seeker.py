from pathfinder import a_star, position, get_heuristic
from Agent import Agent
import GameMaster, uuid, random


class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__path: dict[uuid.UUID, list[position]] = {}
        self.__hiderLastPos: dict[uuid.UUID, position | None] = {}
        self.point = 100

    def move(self, step: int) -> None:
        announcement = GameMaster.GameMaster.seekerGetAnnouncement()
        if announcement:
            for id, pos in announcement.items():
                self.__hiderLastPos[id] = pos
        observed = GameMaster.GameMaster.seekerGetSurrounding()
        for id, pos in observed.items():
            self.__hiderLastPos[id] = pos
        for id, pos in self.__hiderLastPos.items():
            if self._position == pos:
                self.__hiderLastPos[id] = None
                self.__path.pop(id, None)
        self.__path = {}
        
        if (step % 1 == 0):
            for id, pos in self.__hiderLastPos.items():
                if not pos:
                    continue
                self.__path[id] = a_star(self.getPosition(), pos)
                if not self.__path[id]:
                    self.__path.pop(id)
                elif self.__path[id][0] == self.getPosition():
                    self.__path[id].pop(0)

        minID = None
        minLen = float("inf")
        for id, path in self.__path.items():
            if len(path) < minLen:
                minLen = len(path)
                minID = id
        if not minID or len(self.__path[minID]) == 0:
            GameMaster.GameMaster.AgentMove(
                self, random.choice(self._get_posible_moves())
            )
            return
        print(f"{self.getPosition()} {self.__path[minID]}")
        GameMaster.GameMaster.AgentMove(
            self,
            (
                self.__path[minID].pop(0)
                if len(self.__path[minID]) >= 5 or random.random() < 0.90
                else random.choice(self._get_posible_moves())
            ),
        )
        if not self.__path[minID]:
            self.__path.pop(minID)
            self.__hiderLastPos[minID] = None
