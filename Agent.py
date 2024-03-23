from abc import ABC, abstractmethod
import pygame

class position(ABC):
    def __init__(self, x : int, y: int):
        self.x = x
        self.y = y

class Agent:
    def __init__(self, x: int, y: int) -> None:
        self.position = position(x, y)
    
    @abstractmethod
    def move(self):
        pass


class Hider(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.isFound = False
    def move(self):
        pass

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.__hiderLastPos = position(0, 0)
    def move(self):
        pass

class GameMaster:
    def __init__(self, filename: str) -> None:
        with open(filename, 'r') as file:
            self._n, self._m = [int(x) for x in next(file).split()]
            self._map = [[int(x) for x in line[:-1]] for line in file]
            for i in range(self._n):
                for j in range(self._m):
                    if self._map[i][j] == 2:
                        self._hider = Hider(i, j)
                    elif self._map[i][j] == 3:
                        self._seeker = Seeker(i, j)
    def update_screen(self, screen: pygame.Surface):
        for i in range(self._n):
            for j in range(self._m):
                if self._map[i][j] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), (i * 50, j * 50, 50, 50))
                elif self._map[i][j] == 2:
                    pygame.draw.rect(screen, (0, 255, 0), (i * 50, j * 50, 50, 50))
                elif self._map[i][j] == 3:
                    pygame.draw.rect(screen, (255, 0, 0), (i * 50, j * 50, 50, 50))
        pygame.display.flip()

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((self._n * 50, self._m * 50))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            screen.fill((255, 255, 255))
            self.update_screen(screen)
            pygame.time.wait(1000)

if __name__ == '__main__':
    game = GameMaster('map.txt')
    game.play()