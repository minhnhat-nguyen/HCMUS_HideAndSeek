import heapq
class position():
    def __init__(self, x : int, y: int):
        self.x = x
        self.y = y

def get_possible_moves(map : list[list[int]], x : int, y : int) -> list[position]:
    moves : list[position] = []
    n = len(map)
    m = len(map[0])
    if x - 1 >= 0 and map[x - 1][y] != 1:
        moves.append(position(x - 1, y))
    if x + 1 < n and map[x + 1][y] != 1:
        moves.append(position(x + 1, y))
    if y - 1 >= 0 and map[x][y - 1] != 1:
        moves.append(position(x, y - 1))
    if y + 1 < m and map[x][y + 1] != 1:
        moves.append((position(x, y + 1)))
    return moves

def get_heuristic(map : list[list[int]], x : int, y : int, target : position) -> int:
    return abs(x - target.x) + abs(y - target.y)

def a_star(map : list[list[int]], start : position, target : position) -> list[position]:
    n = len(map)
    m = len(map[0])
    visited = [[False for _ in range(m)] for _ in range(n)]
    parent = [[position(-1, -1) for _ in range(m)] for _ in range(n)]
    g = [[float('inf') for _ in range(m)] for _ in range(n)]
    g[start.x][start.y] = 0
    f = [[float('inf') for _ in range(m)] for _ in range(n)]
    f[start.x][start.y] = get_heuristic(map, start.x, start.y, target)
    pq = [(f[start.x][start.y], start)]
    while pq:
        _, current = heapq.heappop(pq)
        if current.x == target.x and current.y == target.y:
            path : list[position] = []
            while current.x != -1 and current.y != -1:
                path.append(current)
                current = parent[current.x][current.y]
            return path[::-1]
        visited[current.x][current.y] = True
        for next in get_possible_moves(map, current.x, current.y):
            if visited[next.x][next.y]:
                continue
            new_g = g[current.x][current.y] + 1
            if new_g < g[next.x][next.y]:
                g[next.x][next.y] = new_g
                f[next.x][next.y] = new_g + get_heuristic(map, next.x, next.y, target)
                parent[next.x][next.y] = current
                heapq.heappush(pq, (f[next.x][next.y], next))
    return []

def bfs(map : list[list[int]], start : position, target : position) -> list[list[int]]
    n = len(map)
    m = len(map[0])
    visited = [[False for _ in range(m)] for _ in range(n)]
    bfs_map = [[0 for _ in range(m)] for _ in range(n)]
    queue = [start]
    visited[start.x][start.y] = True
    while queue:
        current = queue.pop(0)
        if current.x == target.x and current.y == target.y:
            break
        for next in get_possible_moves(map, current.x, current.y):
            if visited[next.x][next.y]:
                continue
            visited[next.x][next.y] = True
            queue.append(next)
            bfs_map[next.x][next.y] = bfs_map[current.x][current.y] + 1
    return bfs_map