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
                    [int(match[0]), int(match[2])],
                    [int(match[1]), int(match[3])],
                ]
            ).astype(int),
            np.array(
                [
                    (int(match[4]) + 10000000000000),
                    (int(match[5]) + 10000000000000),
                ]
            ).astype(int),
        )
    )

total_cost = 0
prizes = 0


def solve(A, b):
    ax, bx, ay, by, px, py = A[0][0], A[0][1], A[1][0], A[1][1], b[0], b[1]

    top = px * ay - py * ax
    divisor = bx * ay - ax * by

    if divisor == 0:
        return 0, 0

    if top % divisor != 0:
        return 0, 0
    B = top // divisor

    top = px * ay - B * bx * ay
    divisor = ax * ay

    if top % divisor != 0:
        return 0, 0

    if divisor == 0:
        return 0, 0

    A = top / divisor
    if A < 0 or B < 0:
        return 0, 0
    return A, B


start_time = time()
for A, b in games:
    # Solve the integer linear system
    x = solve(A, b)
    integer_solution = np.round(x).astype(int)
    total_cost += 3 * integer_solution[0] + integer_solution[1]


print(total_cost)
print("--- %s seconds ---" % (time() - start_time))
