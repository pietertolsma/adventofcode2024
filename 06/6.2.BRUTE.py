from collections import defaultdict


grid = []
with open("data.txt", "r") as file:
    for line in file.readlines():
        grid.append(list(line.strip()))

rows, cols = len(grid), len(grid[0])


def find_start_pos():
    for x in range(cols):
        for y in range(rows):
            if grid[y][x] == "^":
                return [y, x]
    return [-1, -1]


def rotate_90(dy, dx):
    if dy == -1 and dx == 0:
        return [0, 1]
    if dy == 0 and dx == 1:
        return [1, 0]
    if dy == 1 and dx == 0:
        return [0, -1]
    return [-1, 0]


def out_of_bounds(y, x):
    return y < 0 or y >= rows or x < 0 or x >= cols


def simulate(grid, start_y, start_x):
    cur_y, cur_x = start_y, start_x
    dy, dx = -1, 0

    seen = set()
    while not out_of_bounds(cur_y, cur_x):
        if (cur_y, cur_x, dy, dx) in seen:
            return False

        seen.add((cur_y, cur_x, dy, dx))

        next_y, next_x = cur_y + dy, cur_x + dx

        # Step 1: check if inside bounds
        if out_of_bounds(next_y, next_x):
            break

        # Step 2: check if next step is blocked.
        while grid[next_y][next_x] == "#":
            # If so, rotate 90 degrees
            dy, dx = rotate_90(dy, dx)
            next_y, next_x = cur_y + dy, cur_x + dx

        cur_y, cur_x = next_y, next_x

    return True


[startY, startX] = find_start_pos()

count = 0
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == "#" or grid[r][c] == "^":
            continue
        old = grid[r][c]
        grid[r][c] = "#"
        if not simulate(grid, startY, startX):
            count += 1
        grid[r][c] = old

print(count)