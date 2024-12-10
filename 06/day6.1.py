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


def simulate(y, x, dy, dx):
    total_score = 1
    while not out_of_bounds(y, x):
        ny, nx = y + dy, x + dx
        score = 1 if grid[y][x] != "X" else 0

        if out_of_bounds(ny, nx):
            score += score
            break
        for _ in range(3):
            if out_of_bounds(ny, nx):
                score += score
            elif grid[ny][nx] == "#":
                [dy, dx] = rotate_90(dy, dx)
                ny, nx = y + dy, x + dx
            else:
                break

        grid[y][x] = "X"
        y, x = ny, nx
        total_score += score
    return total_score


[startY, startX] = find_start_pos()
score = simulate(startY, startX, -1, 0)
print(score)

Xs = 0
for y in range(rows):
    for x in range(cols):
        if grid[y][x] == "X":
            Xs += 1
print(Xs)
