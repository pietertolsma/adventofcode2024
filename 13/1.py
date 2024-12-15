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


# Try to divide as much as possible with button B,
# such that the remainder is still divisible by button B.
# P = c * A + b * B
# P - b * B = c * A s.t. b is maximized?
# b = (c * A - P) / -B
# b = (c * xA + c * yA - xP - yP) * (-xB - yB)^(-1) = (c * A) / (-B) - P / (-B)
# b" (w.r.t. c) = A / -B

# A / -B = (c*A - P) / -B
# A = c * A - P
# c = (A - P) / A


total_cost = 0
prizes = 0
for A, b in games:
    x, residuals, _, _ = np.linalg.lstsq(A, b)
    integer_solution = np.round(x).astype(int)
    if np.allclose(np.dot(A, integer_solution), b):
        total_cost += integer_solution[0] + integer_solution[1]
        prizes += 1

print(total_cost)
