from pathfinder import a_star, position, get_heuristic
from Agent import Agent
import GameMaster, uuid, random

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__path: dict[uuid.UUID, list[position]] = {}
        self.__hiderLastPos: dict[uuid.UUID, position | None] = {}
    
    def move(self) -> None:
        announcement = GameMaster.GameMaster.seekerGetAnnouncement()
        if announcement:
            for id, pos in announcement.items():
                self.__hiderLastPos[id] = pos
        observed = GameMaster.GameMaster.seekerGetSurrounding()
        for id, pos in observed.items():
            self.__hiderLastPos[id] = pos
            self.__path[id] = a_star(self.getPosition(), pos)[1:]
        for id, pos in self.__hiderLastPos.items():
            if self._position == pos:
                self.__hiderLastPos[id] = None
                self.__path.pop(id, None)
        if not self.__path:
            minID = None
            for id, pos in self.__hiderLastPos.items():
                if pos is None:
                    continue
                if minID is None:
                    minID = id
                    continue
                if self.__hiderLastPos[minID] is None: 
                    continue
                else:
                    minID = id if get_heuristic(self.getPosition(), pos) < get_heuristic(self.getPosition(), self.__hiderLastPos[minID]) else minID
            if minID:
                self.__path[minID] = a_star(self.getPosition(), self.__hiderLastPos[minID])
            else:
                GameMaster.GameMaster.AgentMove(self, random.choice(self._get_posible_moves()))
                return

        minID = None
        minLen = float("inf")
        for id, path in self.__path.items():
            if len(path) < minLen:
                minLen = len(path)
                minID = id
        if not minID or len(self.__path[minID]) == 0:
            GameMaster.GameMaster.AgentMove(self, random.choice(self._get_posible_moves()))
            return
        GameMaster.GameMaster.AgentMove(self, self.__path[minID].pop(0))
        if not self.__path[minID]:
            self.__path.pop(minID)
            self.__hiderLastPos[minID] = None