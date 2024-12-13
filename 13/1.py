import math
import numpy as np
import re

game_pattern = re.compile(
    r"Button A: X\+(\d+), Y\+(\d+)\n"
    r"Button B: X\+(\d+), Y\+(\d+)\n"
    r"Prize: X=(\d+), Y=(\d+)"
)

input_data = ""
games = []
with open("data1.txt", "r") as file:
    input_data = file.read()

matches = game_pattern.findall(input_data)
for match in matches:
    games.append(
        (
            np.array(
                [
                    [int(match[0]) / 3, int(match[2])],
                    [int(match[1]) / 3, int(match[3])],
                ]
            ),
            np.array([int(match[4]), int(match[5])]),
        )
    )


total_cost = 0
prizes = 0
for A, b in games:
    x, residuals, _, _ = np.linalg.lstsq(A, b)
    integer_solution = np.round(x).astype(int)
    if np.allclose(np.dot(A, integer_solution), b):
        total_cost += integer_solution[0] + integer_solution[1]
        prizes += 1

print(total_cost)
