import re
from time import time
import numpy as np

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
    # Scale the first column by 3 to avoid division
    games.append(
        (
            np.array(
                [
                    [int(match[0]), int(match[2]) * 3],
                    [int(match[1]), int(match[3]) * 3],
                ]
            ).astype(int),
            np.array(
                [
                    (int(match[4]) + 10000000000000) * 3,
                    (int(match[5]) + 10000000000000) * 3,
                ]
            ).astype(int),
        )
    )

total_cost = 0
prizes = 0


start_time = time()
for A, b in games:
    # Solve the integer linear system
    x, residuals, _, _ = np.linalg.lstsq(A, b, rcond=None)
    integer_solution = np.round(x).astype(int)

    # Check if the integer solution is valid
    if np.allclose(np.dot(A, integer_solution), b, rtol=0):
        total_cost += integer_solution[0] + integer_solution[1]
        prizes += 1

print(total_cost)
print("--- %s seconds ---" % (time() - start_time))
