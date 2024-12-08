from collections import defaultdict


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


antennas = find_antenna_positions()


def calculate_antinode_position(pos1, pos2):
    dr = pos2[0] - pos1[0]
    dc = pos2[1] - pos1[1]
    return (pos1[0] + 2 * dr, pos1[1] + 2 * dc)


def is_within_bounds(r, c):
    return r >= 0 and r < ROWS and c >= 0 and c < COLS


antinodes = set()
for antenna, positions in antennas.items():
    for r, c in positions:
        for r2, c2 in positions:
            if r == r2 and c == c2:
                continue
            (ra, rc) = calculate_antinode_position((r, c), (r2, c2))
            if is_within_bounds(ra, rc):
                antinodes.add((ra, rc))

print(len(antinodes))
