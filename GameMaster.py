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
    step = 1
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
            GameMaster.__map = [[int(x) for x in line.strip()] for _ in range(self._n) for line in [file.readline()]]
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
        if GameMaster.__seeker.point <= 0:
            return True
        for hider in GameMaster.__hiders:
            if not hider.isFound():
                return False
        return True

    @staticmethod
    def AgentMove(agent: Hider | Seeker, pos: position) -> None:
        if pos not in agent._get_posible_moves(): raise ValueError("Invalid Move")
        agent.point -= 1
        if (type(agent) == Hider and pos == GameMaster.__seeker.getPosition()):
            GameMaster.__seeker.point += 20
            agent.markFound()
            GameMaster.__map[agent.getPosition().x][agent.getPosition().y] = 0
            return
        elif type(agent) == Seeker:
            for hider in GameMaster.__hiders:
                if hider.getPosition() == pos:
                    GameMaster.__seeker.point += 20
                    hider.markFound()
                    GameMaster.__map[hider.getPosition().x][hider.getPosition().y] = 0
                if hider.point <= 0:
                    hider.markFound()
                    GameMaster.__map[hider.getPosition().x][hider.getPosition().y] = 0
        val = 3 if type(agent) == Seeker else 2
        GameMaster.__map[agent.getPosition().x][agent.getPosition().y] = 0
        agent._position = pos
        GameMaster.__map[agent.getPosition().x][agent.getPosition().y] = val

    def __update_screen(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        for i in range(self._n):
            for j in range(self._m):
                pygame.draw.rect(screen, (0, 0, 0), (j * self._blockSize, i * self._blockSize, self._blockSize, self._blockSize), 1)
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
        if GameMaster.step % GameMaster.__hiderAnnounceInterval == 0:
            for agent in GameMaster.__hiders:
                agent.point += GameMaster.__hiderAnnounceInterval + 2
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
        return GameMaster.__seeker.getPosition()
    
    def menu(self, screen: pygame.Surface) -> None:
        background = pygame.image.load("background.jpg")
        background = pygame.transform.scale(background, (self._m * self._blockSize, self._n * self._blockSize))
        screen.blit(background, (0, 0))
        play_button = pygame.Rect(self._m * self._blockSize * 2 / 3, 50, 200, 50)
        pygame.draw.rect(screen, (0, 0, 0), play_button, 1)
        font = pygame.font.Font(None, 36)
        text = font.render("Play", True, (0, 0, 0))
        text_rect = text.get_rect(center=play_button.center)
        screen.blit(text, text_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if play_button.collidepoint(x, y):
                        return
            pygame.display.flip()
        

    def gameLoop(self, screen : pygame.Surface) -> str:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.__update_screen(screen)
            if self.is_game_over():
                if GameMaster.__seeker.point <= 0:
                    return "Hider Win!!"
                else:
                    return "Seeker Wins"
            GameMaster.__seeker.move(self.step)
            if GameMaster.hiderMove:
                for hider in GameMaster.__hiders:
                    if hider.isFound(): continue
                    hider.move(self.step)
            GameMaster.step += 1
            pygame.time.wait(100)

    def play(self):
        pygame.time.Clock().tick(20)
        screen = pygame.display.set_mode((self._m * self._blockSize, self._n * self._blockSize))
        self.menu(screen)
        result = self.gameLoop(screen)
        font = pygame.font.Font(None, int(1 / 8 * self._m * self._blockSize))
        text = font.render(result, True, pygame.color.Color("red"))
        text_rect = text.get_rect(center=(self._m * self._blockSize // 2, self._n * self._blockSize // 2))
        while (True):
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(100)
                

