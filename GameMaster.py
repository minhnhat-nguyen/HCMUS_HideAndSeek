#from Agent import Agent
from Hider import Hider
from Seeker import Seeker
import pygame, copy

class GameMaster:
    def __init__(self, filename: str) -> None:
        self._hider = Hider(0, 0)
        self._seeker = Seeker(0, 0)
        self._turn = 0
        self._seekerAnnounceInterval = 2
        with open(filename, 'r') as file:
            self._n, self._m = [int(x) for x in next(file).split()]
            self._map = [[int(x) for x in line[:-1]] for line in file]
            for i in range(self._n):
                for j in range(self._m):
                    if self._map[i][j] == 2:
                        self._hider = Hider(i, j)
                    elif self._map[i][j] == 3:
                        self._seeker = Seeker(i, j)
        self._hidden_map = copy.deepcopy(self._map)
        self._hidden_map[self._hider.position.x][self._hider.position.y] = 0
        self._hidden_map[self._seeker.position.x][self._seeker.position.y] = 0


    def is_game_over(self) -> bool:
        return self._hider.isFound

    def _update_screen(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        for i in range(self._n):
            for j in range(self._m):
                if self._map[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (j * 50, i * 50, 50, 50))
                elif self._map[i][j] == 2:
                    pygame.draw.rect(screen, (0, 255, 100), (j * 50, i * 50, 50, 50))
                elif self._map[i][j] == 3:
                    pygame.draw.rect(screen, (255, 0, 0), (j * 50, i * 50, 50, 50))
        pygame.display.flip()

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self._m * 50, self._n * 50))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            while True:
                self._update_screen(screen)
                if self.is_game_over():
                    break
                if self._turn % self._seekerAnnounceInterval == 0:
                    self._seeker.hiderLastPos = self._hider.annoucePos()
                else: 
                    self._seeker.hiderLastPos = None
                self._turn += 1
                previousSeekerPos = self._seeker.position
                self._seeker.move(self._hidden_map)
                self._map[previousSeekerPos.x][previousSeekerPos.y] = 0
                self._map[self._seeker.position.x][self._seeker.position.y] = 3
                if self._seeker.position.x == self._hider.position.x and self._seeker.position.y == self._hider.position.y:
                    self._hider.isFound = True
                pygame.time.Clock().tick(20)