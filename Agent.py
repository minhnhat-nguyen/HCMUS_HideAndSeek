from abc import ABC, abstractmethod
import pygame
import random

class position(ABC):
    def __init__(self, x : int, y: int):
        self.x = x
        self.y = y

class Agent:
    def __init__(self, x: int, y: int) -> None:
        self.position = position(x, y)
        self.point = 100
    @abstractmethod
    def move(self, moves : list[position]) -> position:
        pass


class Hider(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.isFound = False
    def move(self, moves : list[position]) -> position:
        self.position = random.choice(moves)
        return self.position

class Seeker(Agent):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.hiderLastPos = position(0, 0)
    def move(self, moves : list[position]) -> position:
        self.position = random.choice(moves)
        return self.position

class GameMaster:
    def __init__(self, filename: str) -> None:
        self._hider = Hider(0, 0)
        self._seeker = Seeker(0, 0)
        with open(filename, 'r') as file:
            self._n, self._m = [int(x) for x in next(file).split()]
            self._map = [[int(x) for x in line[:-1]] for line in file]
            for i in range(self._n):
                for j in range(self._m):
                    if self._map[i][j] == 2:
                        self._hider = Hider(i, j)
                    elif self._map[i][j] == 3:
                        self._seeker = Seeker(i, j)

    def is_game_over(self) -> bool:
        return self._hider.isFound

    def _get_posible_moves(self, ag: Agent) -> list[position]:
        moves : list[position] = []
        x = ag.position.x
        y = ag.position.y
        if x - 1 >= 0 and self._map[x - 1][y] != 1:
            moves.append(position(x - 1, y))
        if x + 1 < self._n and self._map[x + 1][y] != 1:
            moves.append(position(x + 1, y))
        if y - 1 >= 0 and self._map[x][y - 1] != 1:
            moves.append(position(x, y - 1))
        if y + 1 < self._m and self._map[x][y + 1] != 1:
            moves.append((position(x, y + 1)))
        return moves

    def _update_screen(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
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
            while True:
                self._update_screen(screen)
                if self.is_game_over():
                    break
                previousSeekerPos = self._seeker.position
                self._seeker.move(self._get_posible_moves(self._seeker))
                self._map[previousSeekerPos.x][previousSeekerPos.y] = 0
                self._map[self._seeker.position.x][self._seeker.position.y] = 3
                if self._seeker.position.x == self._hider.position.x and self._seeker.position.y == self._hider.position.y:
                    self._hider.isFound = True
                pygame.time.delay(500)

if __name__ == '__main__':
    game = GameMaster('map.txt')
    game.play()