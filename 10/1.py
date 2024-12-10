GRID = []

with open("data.txt", "r") as file:
    for line in file.readlines():
        GRID.append([int(el) for el in list(line.strip())])


ROWS, COLS = len(GRID), len(GRID[0])
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def out_of_bounds(r, c):
    return not (0 <= r and r < ROWS and 0 <= c and c < COLS)


def find_next_positions(cur_r, cur_c, seen):
    res = []
    cur_height = GRID[cur_r][cur_c]

    for dr, dc in DIRS:
        new_r, new_c = cur_r + dr, cur_c + dc
        if (
            not out_of_bounds(new_r, new_c)
            and (new_r, new_c) not in seen
            and (cur_height + 1) == GRID[new_r][new_c]
        ):
            res.append((new_r, new_c))
    return res


def find_reachable_nines_from_pos(start_r, start_c):
    seen = set()

    queue = [(start_r, start_c)]

    count = 0
    while len(queue):
        (cur_r, cur_c) = queue.pop()
        seen.add((cur_r, cur_c))

        for new_r, new_c in find_next_positions(cur_r, cur_c, seen):
            queue.append((new_r, new_c))

        if GRID[cur_r][cur_c] == 9:
            count += 1
    return count


total_sum = 0
for r in range(ROWS):
    for c in range(COLS):
        if GRID[r][c] == 0:
            total_sum += find_reachable_nines_from_pos(r, c)
print(total_sum)
