grid = []

with open("data.txt", "r") as file:
    for line in file.readlines():
        grid.append(list(line.strip()))

ROWS, COLS = len(grid), len(grid[0])


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
visited = [[False for _ in range(COLS)] for _ in range(ROWS)]


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def dfs_region_search(start_r, start_c):
    visited[start_r][start_c] = True

    symbol = grid[start_r][start_c]

    area, fences = 1, 4
    neighbors = []
    for dr, dc in directions:
        nr, nc = start_r + dr, start_c + dc
        if not in_bounds(nr, nc):
            continue
        if grid[nr][nc] == symbol:
            fences -= 1
            neighbors.append((nr, nc))

    for nr, nc in neighbors:
        if visited[nr][nc]:
            continue
        area2, fences2 = dfs_region_search(nr, nc)
        area += area2
        fences += fences2

    return area, fences


def aggregate_regions():
    sum = 0
    for r in range(ROWS):
        for c in range(COLS):
            if visited[r][c]:
                continue
            area, fences = dfs_region_search(r, c)
            sum += area * fences

    return sum


print(aggregate_regions())
