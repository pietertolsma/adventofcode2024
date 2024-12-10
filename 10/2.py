from time import time


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


def find_distinct_paths_to_nine(start_r, start_c):
    queue = [(start_r, start_c, set())]

    count = 0
    while len(queue):
        (cur_r, cur_c, seen) = queue.pop()

        seen.add((cur_r, cur_c))
        if GRID[cur_r][cur_c] == 9:
            count += 1
            continue

        next_positions = find_next_positions(cur_r, cur_c, seen)
        # How many of these positions lead to 9?
        for new_r, new_c in next_positions:
            queue.append((new_r, new_c, set(seen)))

    return count


total_sum = 0
start_time = time()
for r in range(ROWS):
    for c in range(COLS):
        if GRID[r][c] == 0:
            total_sum += find_distinct_paths_to_nine(r, c)
print(total_sum)
print("--- %s seconds ---" % (time() - start_time))
