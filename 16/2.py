from enum import Enum
from heapq import heappush, heappop
from time import time

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


def print_grid():
    with open("output.txt", "w") as file:
        for line in grid:
            file.write("".join(line) + "\n")


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
    if target_dir.value == direction:
        return 1.0
    return 1001.0


def a_star(grid, start, goal):
    closed_set = {}
    open_set = []
    best_score = float("inf")
    heappush(open_set, (0.0, start, Direction.EAST.value, set()))

    best_paths = set([start])
    seen = set()
    while open_set:
        score, current, dir, path = heappop(open_set)
        if current == goal and score <= best_score:
            best_score = score
            best_paths = best_paths.union(path)
            continue

        if score > best_score:
            continue
        if closed_set.get((current, dir), float("inf")) > best_score:
            continue
        seen.add((current, dir))
        closed_set[(current, dir)] = score
        for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_dir = dirmap[neighbor]
            diff = abs(new_dir.value - dir)
            if diff == 2:
                continue
            neighbor_pos = (current[0] + neighbor[0], current[1] + neighbor[1])
            new_score = score + heuristic(neighbor, dir)
            if (
                in_range(neighbor_pos[0], neighbor_pos[1])
                and grid[neighbor_pos[0]][neighbor_pos[1]] != "#"
                and closed_set.get((neighbor_pos, new_dir), float("inf")) >= new_score
            ):
                closed_set[(neighbor_pos, new_dir)] = new_score
                path_cpy = path.copy()
                path_cpy.add(neighbor_pos)
                heappush(
                    open_set,
                    (
                        new_score,
                        neighbor_pos,
                        dirmap[neighbor].value,
                        path_cpy,
                    ),
                )

    for r, c in best_paths:
        grid[r][c] = "O"
    return best_paths


def find_symbol_positions(symbol: str):
    res = []
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if grid[r][c] == symbol:
                res.append((r, c))
    return res


start_time = time()
start = find_symbol_positions("S")[0]
goal = find_symbol_positions("E")[0]
print(start, goal)
path = a_star(grid, start, goal)

print("--- %s seconds ---" % (time() - start_time))
print_grid()
print(len(path))
