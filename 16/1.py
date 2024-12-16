from enum import Enum
from heapq import heappush, heappop

file = "data.txt"
grid, moves = [], []
with open(file, "r") as file:
    part1 = True
    for line in file.readlines():
        if line == "\n":
            part1 = False
            continue
        if part1:
            grid.append(list(line.strip()))
        else:
            moves += list(line.strip())
ROWS, COLS = len(grid), len(grid[0])


def in_range(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


dirmap = {
    (-1, 0): Direction.NORTH,
    (0, -1): Direction.WEST,
    (1, 0): Direction.SOUTH,
    (0, 1): Direction.EAST,
}


def heuristic(dir, direction):
    target_dir = dirmap[dir]
    if target_dir.value == direction.value:
        return 1.0
    return 1001.0


def a_star(grid, start, goal):
    closed_set = set()
    came_from = {}
    g_score = {(start, Direction.EAST): 0.0}
    open_set = []
    heappush(open_set, (0.0, start, Direction.EAST))

    while open_set:
        score, current, dir = heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return score, path

        closed_set.add((current, dir))
        for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_dir = dirmap[neighbor]
            diff = abs(new_dir.value - dir.value)
            if diff == 2:
                continue
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])
            if (
                in_range(neighbor_pos[0], neighbor_pos[1])
                and grid[neighbor_pos[0]][neighbor_pos[1]] != "#"
                and (neighbor_pos, new_dir) not in closed_set
            ):
                tentative_g_score = g_score[(current, dir)] + heuristic(neighbor, dir)
                if neighbor_pos not in [
                    i[1] for i in open_set
                ] or tentative_g_score < g_score.get((neighbor_pos, new_dir), 0):
                    came_from[neighbor_pos] = current
                    g_score[(neighbor_pos, new_dir)] = tentative_g_score
                    heappush(
                        open_set,
                        (
                            g_score[(neighbor_pos, new_dir)],
                            neighbor_pos,
                            dirmap[neighbor],
                        ),
                    )

    return None


def find_symbol_positions(symbol: str):
    res = []
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if grid[r][c] == symbol:
                res.append((r, c))
    return res


start = find_symbol_positions("S")[0]
goal = find_symbol_positions("E")[0]
print(start, goal)
path = a_star(grid, start, goal)
print(path)
