import re
import numpy as np

robots = []

input_txt = ""
input_file = "data.txt"
with open(input_file, "r") as file:
    input_txt = file.read()

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


TURNS = 100

lowest_std, index = 10, -1


for i in range(TURNS):
    positions += speeds
    positions = np.mod(positions, (ROWS, COLS))

score = calculate_quadrants(positions)
print(score)
