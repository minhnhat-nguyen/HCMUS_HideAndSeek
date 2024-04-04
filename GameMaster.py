from Hider import Hider
from Seeker import Seeker
from pathfinder import bresenham, position
import pygame, copy, uuid

class GameMaster:
    __map: list[list[int]]
    hidden_map: list[list[int]]
    __hiderAnnounceInterval = 5
    __seekerObserveRange = 3
    __hiderObserveRange = 2
    __turn = 0
    __seeker: Seeker = Seeker(0, 0)
    __hiders: list[Hider] = []
    hiderMove = True
    def __init__(self, filename: str) -> None:
        with open(filename, "r") as file:
            pygame.init()
            self._n, self._m = [int(x) for x in next(file).split()]
            resolution = pygame.display.Info()
            self._blockSize = min(resolution.current_w // (self._m + 2), 
                                  resolution.current_h // (self._n + 2)) 
            GameMaster.__map = [[int(x) for x in line[:-1]] for line in file]
            for i in range(self._n):
                for j in range(self._m):
                    if GameMaster.__map[i][j] == 2:
                        GameMaster.__hiders.append(Hider(i, j))
                    elif GameMaster.__map[i][j] == 3:
                        GameMaster.__seeker = Seeker(i, j)
        GameMaster.hidden_map = copy.deepcopy(GameMaster.__map)
        GameMaster.hidden_map[GameMaster.__seeker.getPosition().x][
            GameMaster.__seeker.getPosition().y
        ] = 0
        for hider in GameMaster.__hiders:
            GameMaster.hidden_map[hider.getPosition().x][hider.getPosition().y] = 0

    def is_game_over(self) -> bool:
        for hider in GameMaster.__hiders:
            if not hider.isFound():
                return False
        return True

    @staticmethod
    def AgentMove(agent: Hider | Seeker, pos: position) -> None:
        if pos not in agent._get_posible_moves(): raise ValueError("Invalid Move")
        if (type(agent) == Hider and pos == GameMaster.__seeker.getPosition()):
            agent.markFound()
            GameMaster.__map[agent.getPosition().x][agent.getPosition().y] = 0
            return
        elif type(agent) == Seeker:
            for hider in GameMaster.__hiders:
                if hider.getPosition() == pos:
                    hider.markFound()
                    GameMaster.__map[hider.getPosition().x][hider.getPosition().y] = 0
                    return
        val = GameMaster.__map[agent.getPosition().x][agent.getPosition().y]
        GameMaster.__map[agent.getPosition().x][agent.getPosition().y] = 0
        agent._position = pos
        GameMaster.__map[agent.getPosition().x][agent.getPosition().y] = val
        


    def __update_screen(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        for i in range(self._n):
            for j in range(self._m):
                if GameMaster.__map[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (j * self._blockSize, i * self._blockSize, self._blockSize, self._blockSize))
                elif GameMaster.__map[i][j] == 2:
                    pygame.draw.rect(screen, (0, 255, 100), (j * self._blockSize, i * self._blockSize, self._blockSize, self._blockSize))
                elif GameMaster.__map[i][j] == 3:
                    pygame.draw.rect(screen, (255, 0, 0), (j * self._blockSize, i * self._blockSize, self._blockSize, self._blockSize))
        pygame.display.flip()

    @staticmethod
    def seekerGetSurrounding() -> dict[uuid.UUID, position]:
        InSight: dict[uuid.UUID, position] = {}
        for hider in GameMaster.__hiders:
            if hider.isFound():
                continue
            if not (
                abs(GameMaster.__seeker.getPosition().x - hider.getPosition().x)
                <= GameMaster.__seekerObserveRange
                and abs(GameMaster.__seeker.getPosition().y - hider.getPosition().y)
                <= GameMaster.__seekerObserveRange
            ):
                continue
            isObserable = True
            for pos in bresenham(
                GameMaster.__seeker.getPosition(), hider.getPosition()
            ):
                if GameMaster.__map[pos.x][pos.y] == 1:
                    isObserable = False
                    break
            if isObserable:
                InSight[hider.id] = hider.getPosition()
        return InSight
    

    @staticmethod
    def seekerGetAnnouncement() -> dict[uuid.UUID, position | None] | None:
        if GameMaster.__turn % GameMaster.__hiderAnnounceInterval == 0:
            return {
                hider.id: hider.announcePos()[1] for hider in GameMaster.__hiders
            }
        return None

    @staticmethod
    def hiderGetSurrounding(hider: Hider) -> position | None:
        if hider.isFound():
            return None
        if not (
            abs(GameMaster.__seeker.getPosition().x - hider.getPosition().x)
            <= GameMaster.__hiderObserveRange
            and abs(GameMaster.__seeker.getPosition().y - hider.getPosition().y)
            <= GameMaster.__hiderObserveRange
        ):
            return None
        for pos in bresenham(GameMaster.__seeker.getPosition(), hider.getPosition()):
            if GameMaster.__map[pos.x][pos.y] == 1:
                return None
        return hider.getPosition()

    def play(self):
        pygame.time.Clock().tick(20)
        screen = pygame.display.set_mode((self._m * self._blockSize, self._n * self._blockSize))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.__update_screen(screen)
            if self.is_game_over():
                print("Game Over")
            GameMaster.__seeker.move()
            if GameMaster.hiderMove:
                for hider in GameMaster.__hiders:
                    if hider.isFound(): continue
                    hider.move()

            GameMaster.__turn += 1
            pygame.time.wait(100)
