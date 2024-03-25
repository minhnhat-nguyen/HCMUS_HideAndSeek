from pathfinder import a_star, position, get_heuristic
from Agent import Agent
import GameMaster

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__path : list[position] = []
        self.__target : position = position(-1, -1)
        self.__hiderLastPos : list[position] = []
        self.__hiderInSight : list[position] = []

    def move(self) -> position:
        self.__hiderInSight = GameMaster.GameMaster.seekerGetSurrounding()
        annc_list : list[position] | None = GameMaster.GameMaster.seekerGetAnnouncement()
        if annc_list:
            self.__hiderLastPos = annc_list
        if len(self.__hiderInSight) != 0:
            minIndex = min(range(len(self.__hiderInSight)), 
                           key=lambda i: get_heuristic(self._position, self.__hiderInSight[i]))
        else:
            minIndex = min(range(len(self.__hiderLastPos)), 
                           key=lambda i: get_heuristic(self._position, self.__hiderLastPos[i]))
        if self.__target != self.__hiderLastPos[minIndex]:
            self.__target = self.__hiderLastPos[minIndex]
            self.__path = a_star(self._position, self.__target)
        if self.__path:
            self._position = self.__path.pop(0)
        print(self._position, self.__target, self.__hiderInSight, self.__hiderLastPos)
        return self._position
