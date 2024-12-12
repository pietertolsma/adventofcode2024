from time import time


grid = []

with open("data.txt", "r") as file:
    for line in file.readlines():
        grid.append(list(line.strip()))

ROWS, COLS = len(grid), len(grid[0])


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def is_same_symbol(target, r, c):
    return in_bounds(r, c) and target == grid[r][c]


def dfs_region_search(start_r, start_c):
    visited[start_r][start_c] = True

    symbol = grid[start_r][start_c]
    queue = [(start_r, start_c)]
    total_area, total_fences = 0, 0

    while len(queue):
        (cur_r, cur_c) = queue.pop(0)
        total_area += 1

        # fences = 4
        neighbors = [False, False, False, False]
        for i, (dr, dc) in enumerate(directions):
            nr, nc = cur_r + dr, cur_c + dc

            if is_same_symbol(symbol, nr, nc):
                # We are stopping the fence from
                # the left hand side and right hand side.
                neighbors[i] = True
                if not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
        # Count how many corners
        outer_corners = 0
        inner_corners = 0
        for i, has_neigh in enumerate(neighbors):
            left_pos = i - 1 if i >= 1 else 3
            if not neighbors[left_pos] and not has_neigh:
                outer_corners += 1

            if neighbors[left_pos] and has_neigh:
                dr, dc = (
                    directions[i][0] + directions[left_pos][0],
                    directions[i][1] + directions[left_pos][1],
                )
                if grid[cur_r + dr][cur_c + dc] != symbol:
                    inner_corners += 1

        total_fences += outer_corners + inner_corners

    return total_area, total_fences


def aggregate_regions():
    sum = 0
    for r in range(ROWS):
        for c in range(COLS):
            if visited[r][c]:
                continue
            area, fences = dfs_region_search(r, c)

            sum += area * fences

    return sum


start_time = time()
print(aggregate_regions())
print("--- %s seconds ---" % (time() - start_time))
