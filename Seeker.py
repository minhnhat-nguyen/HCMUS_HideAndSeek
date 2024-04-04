from pathfinder import a_star, position, get_heuristic
from Agent import Agent
import GameMaster, uuid, random

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__path: dict[uuid.UUID, list[position]] = {}
        self.__hiderLastPos: dict[uuid.UUID, position | None] = {}
    
    def move(self) -> position:
        announcement = GameMaster.GameMaster.seekerGetAnnouncement()
        if announcement:
            for id, pos in announcement.items():
                self.__hiderLastPos[id] = pos
        observed = GameMaster.GameMaster.seekerGetSurrounding()
        for id, pos in observed.items():
            self.__hiderLastPos[id] = pos
            self.__path[id] = a_star(self.getPosition(), pos)[1:]
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
            if not minID:
                self._position = random.choice(self._get_posible_moves())
                return self._position
            else:
                self.__path[minID] = a_star(self.getPosition(), self.__hiderLastPos[minID])

        #find shortest list in path
        minID = None
        minLen = float("inf")
        for id, path in self.__path.items():
            if len(path) < minLen:
                minLen = len(path)
                minID = id
        self._position = self.__path[minID].pop(0)
        if not self.__path[minID]:
            self.__path.pop(minID)
            self.__hiderLastPos[minID] = None
        return self._position
