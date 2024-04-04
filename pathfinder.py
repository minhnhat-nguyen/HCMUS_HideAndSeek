from __future__ import annotations
import heapq
import GameMaster
import math


class position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, position):
            return False
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: position) -> bool:
        return self.x < other.x or (self.x == other.x and self.y < other.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __add__(self, other: position) -> position:
        return position(self.x + other.x, self.y + other.y)


class PriorityQueueItem:
    def __init__(self, f_score: float, pos: position) -> None:
        self.f_score = f_score
        self.pos = pos

    def __lt__(self, other: PriorityQueueItem):
        return self.f_score < other.f_score


def get_possible_moves(x: int, y: int) -> list[position]:
    moves: list[position] = [position(x, y)]
    n = len(GameMaster.GameMaster.hidden_map)
    m = len(GameMaster.GameMaster.hidden_map[0])
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (
                0 <= x + i < n
                and 0 <= y + j < m
                and GameMaster.GameMaster.hidden_map[x + i][y + j] != 1
            ):
                moves.append(position(x + i, y + j))
    return moves


def get_heuristic(start: position, target: position) -> float:
    return math.hypot(start.x - target.x, start.y - target.y)


def a_star(start: position, target: position) -> list[position]:
    n = len(GameMaster.GameMaster.hidden_map)
    m = len(GameMaster.GameMaster.hidden_map[0])
    visited = [[False for _ in range(m)] for _ in range(n)]
    parent: list[list[position | None]] = [[None for _ in range(m)] for _ in range(n)]
    g = [[float("inf") for _ in range(m)] for _ in range(n)]
    g[start.x][start.y] = 0
    f = [[float("inf") for _ in range(m)] for _ in range(n)]
    f[start.x][start.y] = get_heuristic(start, target)
    pq = [PriorityQueueItem(f[start.x][start.y], start)]
    while pq:
        current = heapq.heappop(pq).pos
        if current.x == target.x and current.y == target.y:
            path: list[position] = []
            while current is not None:
                path.append(current)
                current = parent[current.x][current.y]
            return path[::-1]
        visited[current.x][current.y] = True
        for next in get_possible_moves(current.x, current.y):
            if visited[next.x][next.y]:
                continue
            new_g = g[current.x][current.y] + 1
            if new_g < g[next.x][next.y]:
                g[next.x][next.y] = new_g
                f[next.x][next.y] = new_g + get_heuristic(next, target)
                parent[next.x][next.y] = current
                heapq.heappush(pq, PriorityQueueItem(f[next.x][next.y], next))
    return []


def bfs(start: position, target: list[position]) -> list[list[int]]:
    n = len(GameMaster.GameMaster.hidden_map)
    m = len(GameMaster.GameMaster.hidden_map[0])
    visited = [[False for _ in range(m)] for _ in range(n)]
    bfs_map = [[0 for _ in range(m)] for _ in range(n)]
    queue = [start]
    visited[start.x][start.y] = True
    while queue:
        current = queue.pop(0)
        if current in target:
            target.remove(current)
            if not target:
                return bfs_map
        for next in get_possible_moves(current.x, current.y):
            if visited[next.x][next.y]:
                continue
            visited[next.x][next.y] = True
            queue.append(next)
            bfs_map[next.x][next.y] = bfs_map[current.x][current.y] + 1
    return bfs_map


def bresenham(p1: position, p2: position) -> list[position]:
    a = position(p1.x, p1.y)
    b = position(p2.x, p2.y)
    m = abs(b.y - a.y)
    n = abs(b.x - a.x)
    dx = 1 if a.x < b.x else -1
    dy = 1 if a.y < b.y else -1
    error = 0
    path: list[position] = []
    if n > m:
        for x in range(a.x, b.x, dx):
            path.append(position(x, a.y))
            error += m
            if 2 * error >= n:
                a.y += dy
                error -= n
    else:
        for y in range(a.y, b.y, dy):
            path.append(position(a.x, y))
            error += n
            if 2 * error >= m:
                a.x += dx
                error -= m
    path.append(b)
    return path
