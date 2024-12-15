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


def find_first_free_spot(cur_r, cur_c, dr, dc):
    cur_r, cur_c = cur_r + dr, cur_c + dc
    while in_range(cur_r, cur_c) and grid[cur_r][cur_c] != "#":
        if grid[cur_r][cur_c] == ".":
            return (cur_r, cur_c)
        cur_r += dr
        cur_c += dc

    return -1, -1


def move_boxes(from_r, from_c, free_r, free_c):
    grid[from_r][from_c] = "@"
    if from_r == free_r and from_c == free_c:
        return
    grid[free_r][free_c] = "O"


def print_grid():
    with open("output.txt", "w") as file:
        for line in grid:
            file.write("".join(line) + "\n")


def simulate_robot(r, c):
    dirmap = {"^": (-1, 0), "<": (0, -1), ">": (0, 1), "v": (1, 0)}
    for move in moves:
        dr, dc = dirmap[move]
        free_r, free_c = find_first_free_spot(r, c, dr, dc)
        if free_r != -1 and free_c != -1:
            grid[r][c] = "."
            r += dr
            c += dc
            move_boxes(r, c, free_r, free_c)
    print_grid()


start_r, start_c = find_symbol_positions("@")[0]
simulate_robot(start_r, start_c)
boxes = find_symbol_positions("O")
final_score = calculate_final_score(boxes)
print(final_score)
