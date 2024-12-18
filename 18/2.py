import re
import numpy as np
from heapq import heapify, heappush, heappop

filename = "data.txt"
points = []
with open(filename, "r") as file:
    for line in file.readlines():
        a, b = line.strip().split(",")
        print(a, b)
        points.append([int(b), int(a)])

ROWS, COLS = (71, 71) if filename == "data.txt" else (7, 7)
TIME = len(points) if filename == "data.txt" else len(points)

grid = np.zeros((ROWS, COLS, TIME)).astype(bool)


def fill_grid():
    for i in range(1, TIME):
        grid[:, :, i] = grid[:, :, i - 1].copy()
        r, c = points[i - 1]
        grid[r, c, i] = True


def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS


def valid_move(new_time, r, c):
    return in_bounds(r, c) and not grid[r][c][new_time]


def dijkstra(start_time):
    queue = [(start_time, 0, 0, 0)]
    heapify(queue)

    visited = np.zeros((ROWS, COLS, TIME)).astype(bool)
    while queue:
        time, steps, r, c = heappop(queue)
        if r == (ROWS - 1) and c == (COLS - 1):
            return True, steps, r, c
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if not valid_move(time, nr, nc) or visited[nr, nc, time]:
                continue
            visited[nr, nc, time] = True
            heappush(queue, (time, steps + 1, nr, nc))
    return False, 0, 0, 0


def print_grid(time):
    with open("output.txt", "w") as file:
        for r in range(ROWS):
            file.write(
                "".join([" " if not el else "#" for el in grid[r, :, time]]) + "\n"
            )


fill_grid()
print_grid(1024)

# At time = 3030 no path possible.


start_time = 1024
for time in range(start_time, 10000):
    status, steps, r, c = dijkstra(time)
    if not status:
        print(time, points[time - 1][::-1])
        break
    else:
        print(f"{time=} / {TIME} {steps=}")
