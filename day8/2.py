from collections import defaultdict
import time

grid = []
with open("data.txt", "r") as file:
    for line in file.readlines():
        grid.append(list(line.strip()))

ROWS, COLS = len(grid), len(grid[0])


def find_antenna_positions():
    antennas = defaultdict(list)
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != ".":
                antennas[grid[r][c]].append((r, c))
    return antennas


def is_within_bounds(r, c):
    return r >= 0 and r < ROWS and c >= 0 and c < COLS


def calculate_antinode_positions(pos1, pos2):
    dr = pos2[0] - pos1[0]
    dc = pos2[1] - pos1[1]
    positions = []
    ra, rc = pos1[0], pos1[1]
    while is_within_bounds(ra, rc):
        positions.append((ra, rc))
        ra += dr
        rc += dc
    return positions


start_time = time.time()
antennas = find_antenna_positions()
antinodes = set()
for antenna, positions in antennas.items():
    for r, c in positions:
        for r2, c2 in positions:
            if r == r2 and c == c2:
                continue
            anti_positions = calculate_antinode_positions((r, c), (r2, c2))
            for ra, rc in anti_positions:
                antinodes.add((ra, rc))

print(len(antinodes))
print("--- %s seconds ---" % (time.time() - start_time))
