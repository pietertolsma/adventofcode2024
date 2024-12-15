import matplotlib.pyplot as plt
import re
import numpy as np
import os

robots = []

input_txt = ""
input_file = "data.txt"
with open(input_file, "r") as file:
    input_txt = file.read()

if os.path.exists("output.txt"):
    os.remove("output.txt")

pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)\n")
matches = pattern.findall(input_txt)

positions, speeds = [], []
for match in matches:
    positions.append(np.array([match[1], match[0]]).astype(int))
    speeds.append(np.array([match[3], match[2]]).astype(int))

positions, speeds = np.vstack(positions), np.vstack(speeds)

ROWS, COLS = 103, 101
if input_file == "data0.txt":
    ROWS, COLS = 7, 11


def draw_map(positions, rows, cols):
    grid = [[" " for _ in range(cols)] for _ in range(rows)]

    for row, col in positions:
        grid[row][col] = "X"

    # Convert the grid to a string representation
    map_str = "\n".join(["".join(row) for row in grid])
    with open("output.txt", "a") as file:
        file.write(map_str + f"\n===={i+1}\n\n")

    return map_str


def calculate_quadrants(positions):
    total_score = 1

    for qc in [0, 1]:
        for qr in [0, 1]:
            start_r, end_r = 1 + ROWS // 2 if qr == 1 else 0, (qr + 1) * ROWS // 2
            start_c, end_c = 1 + COLS // 2 if qc == 1 else 0, (qc + 1) * COLS // 2

            mask_r = (positions[:, 0] >= start_r) & (positions[:, 0] < end_r)
            mask_c = (positions[:, 1] >= start_c) & (positions[:, 1] < end_c)
            mask = mask_r & mask_c
            total_score *= mask.sum()

    return total_score


def calculate_max_connected_elements(positions):
    pos_set = set((r, c) for r, c in positions)
    visited = set()
    dirs = [(-1, -1), (1, 1), (-1, 1), (1, -1)]
    best = 0

    def dfs(r, c):
        if (r, c) not in pos_set or (r, c) in visited:
            return 0
        score = 1
        visited.add((r, c))

        for dr, dc in dirs:
            score += dfs(r + dr, c + dc)
        return score

    for [r, c] in positions:
        best = max(dfs(r, c), best)
    return best


TURNS = 10000

scores = []

for i in range(TURNS):
    positions += speeds
    positions = np.mod(positions, (ROWS, COLS))

    max_connected = calculate_max_connected_elements(positions)
    scores.append(max_connected)

    print(i, max_connected)
    if max_connected > 10:
        # print(max_connected)
        draw_map(positions, ROWS, COLS)


# print(scores)
plt.plot(scores)
plt.show()
# print(total_score)
