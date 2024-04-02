from Hider import Hider
from Seeker import Seeker
from pathfinder import bresenham, position
import pygame, copy


class GameMaster:
    __map: list[list[int]]
    hidden_map: list[list[int]]
    __hiderAnnounceInterval = 5
    __seekerObserveRange = 3
    __hiderObserveRange = 2
    __turn = 0
    __seeker: Seeker = Seeker(0, 0)
    __hiders: list[Hider] = []

    def __init__(self, filename: str) -> None:
        with open(filename, "r") as file:
            self._n, self._m = [int(x) for x in next(file).split()]
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

    def __update_screen(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        for i in range(self._n):
            for j in range(self._m):
                if GameMaster.__map[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (j * 50, i * 50, 50, 50))
                elif GameMaster.__map[i][j] == 2:
                    pygame.draw.rect(screen, (0, 255, 100), (j * 50, i * 50, 50, 50))
                elif GameMaster.__map[i][j] == 3:
                    pygame.draw.rect(screen, (255, 0, 0), (j * 50, i * 50, 50, 50))
        pygame.display.flip()

    @staticmethod
    def seekerGetSurrounding() -> list[position]:
        InSight: list[position] = []
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
                InSight.append(hider.getPosition())
        return InSight

    @staticmethod
    def seekerGetAnnouncement() -> list[position] | None:
        if GameMaster.__turn % GameMaster.__hiderAnnounceInterval == 0:
            return [
                hider.annoucePos()
                for hider in GameMaster.__hiders
                if not hider.isFound()
            ]
        return None

    @staticmethod
    def hiderGetSurrounding(hider: Hider) -> list[position]:
        InSight: list[position] = []
        if hider.isFound():
            return InSight
        if not (
            abs(GameMaster.__seeker.getPosition().x - hider.getPosition().x)
            <= GameMaster.__hiderObserveRange
            and abs(GameMaster.__seeker.getPosition().y - hider.getPosition().y)
            <= GameMaster.__hiderObserveRange
        ):
            return InSight
        for pos in bresenham(GameMaster.__seeker.getPosition(), hider.getPosition()):
            if GameMaster.__map[pos.x][pos.y] == 1:
                return InSight
        return [GameMaster.__seeker.getPosition()]

    def play(self):
        pygame.init()
        pygame.time.Clock().tick(20)
        screen = pygame.display.set_mode((self._m * 50, self._n * 50))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.__update_screen(screen)
            if self.is_game_over():
                print("Game Over")
                break
            GameMaster.__map[GameMaster.__seeker.getPosition().x][
                GameMaster.__seeker.getPosition().y
            ] = 0
            GameMaster.__seeker.move()
            GameMaster.__map[GameMaster.__seeker.getPosition().x][
                GameMaster.__seeker.getPosition().y
            ] = 3
            for hider in GameMaster.__hiders:
                if hider.getPosition() == GameMaster.__seeker.getPosition():
                    hider.markFound()
            GameMaster.__turn += 1
            pygame.time.wait(100)
