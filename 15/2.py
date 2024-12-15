from collections import deque

import copy
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


def grow_grid():
    new_grid = [["." for _ in range(COLS * 2)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            sym = grid[r][c]
            if sym == "#":
                new_grid[r][2 * c] = "#"
                new_grid[r][2 * c + 1] = "#"
            if sym == "O":
                new_grid[r][2 * c] = "["
                new_grid[r][2 * c + 1] = "]"
            if sym == "@":
                new_grid[r][2 * c] = "@"
    return new_grid


grid = grow_grid()
ROWS, COLS = ROWS, 2 * COLS


def in_range(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def find_symbol_positions(symbol: str):
    res = []
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if grid[r][c] == symbol:
                res.append((r, c))
    return res


def calculate_final_score(boxes):
    score = 0
    for [r, c] in boxes:
        score += 100 * r + c
    return score


def shift_positions(positions, dr, dc):
    for [r, c] in positions[::-1]:
        grid[r + dr][c + dc] = grid[r][c]
        grid[r][c] = "."
    return grid


def print_grid():
    with open("output.txt", "w") as file:
        for line in grid:
            file.write("".join(line) + "\n")


def find_free_positions(start_r, start_c, dr, dc):
    queue = deque([(start_r, start_c)])
    seen = set()
    free_positions = []

    while queue:
        r, c = queue.popleft()

        if not in_range(r, c) or (r, c) in seen:
            continue

        seen.add((r, c))

        if grid[r][c] == ".":
            continue
        elif grid[r][c] == "#":
            return False, []

        free_positions.append((r, c))
        if dr == 0:
            if grid[r][c] == "[":
                free_positions.append((r, c + 1))
                queue.append((r, c + 2))
            elif grid[r][c] == "]":
                free_positions.append((r, c - 1))
                queue.append((r, c - 2))
        else:
            loffset = -1 if grid[r][c] == "]" else 1
            queue.append((r, c + loffset))
            queue.append((r + dr, c + dc))

    return True, free_positions


def simulate_robot(r, c):
    dirmap = {"^": (-1, 0), "<": (0, -1), ">": (0, 1), "v": (1, 0)}
    for i, move in enumerate(moves):
        dr, dc = dirmap[move]
        valid, positions = find_free_positions(r + dr, c + dc, dr, dc)
        if valid:
            shift_positions(positions, dr, dc)
            grid[r + dr][c + dc] = "@"
            grid[r][c] = "."
            r += dr
            c += dc


start_time = time()
start_r, start_c = find_symbol_positions("@")[0]
print_grid()
simulate_robot(start_r, start_c)
boxes = find_symbol_positions("[")
final_score = calculate_final_score(boxes)

print(final_score)
print("--- %s seconds ---" % (time() - start_time))
print_grid()
