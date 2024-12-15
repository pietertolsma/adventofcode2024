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
    original = copy.deepcopy(grid)
    pos = set(positions)

    for [r, c] in positions:
        if (r - dr, c - dc) not in pos:
            grid[r][c] = "."
        grid[r + dr][c + dc] = original[r][c]
    return grid


def print_grid():
    with open("output.txt", "w") as file:
        for line in grid:
            file.write("".join(line) + "\n")


def find_free_positions(r, c, dr, dc, seen):
    if not in_range(r, c):
        return False, []
    if (r, c) in seen:
        return True, []
    if grid[r][c] == ".":
        return True, []
    if grid[r][c] == "#":
        return False, []

    seen.add((r, c))
    if grid[r][c] == "[" and dr == 0:
        stat, others = find_free_positions(r + dr, c + 2, dr, dc, seen)
        return stat, [(r, c), (r + dr, c + dc)] + others
    if grid[r][c] == "]" and dr == 0:
        stat, others = find_free_positions(r + dr, c - 2, dr, dc, seen)
        return stat, [(r, c), (r + dr, c + dc)] + others

    loffset = -1 if grid[r][c] == "]" else 1
    stat, side_positions = find_free_positions(r, c + loffset, dr, dc, seen)
    stat2, side_positions2 = find_free_positions(r + dr, c + dc, dr, dc, seen)
    merged = list(set(side_positions) | set(side_positions2))
    if not stat2 or not stat:
        return False, []
    return True, [(r, c)] + merged


def simulate_robot(r, c):
    dirmap = {"^": (-1, 0), "<": (0, -1), ">": (0, 1), "v": (1, 0)}
    for i, move in enumerate(moves):
        dr, dc = dirmap[move]
        valid, positions = find_free_positions(r + dr, c + dc, dr, dc, set())
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
