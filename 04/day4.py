lines = []
with open("data.txt", "r") as file:
    for line in file.readlines():
        lines.append(list(line.strip()))

rows, cols = len(lines), len(lines[0])


def has_word(word, x, y, dx, dy):
    if dx == 0 and dy == 0:
        return False
    if len(word) == 0:
        return True

    if lines[y][x] != word[0]:
        return False
    if len(word) == 1:
        return True
    nx, ny = x + dx, y + dy
    if nx < 0 or nx > cols - 1 or ny < 0 or ny > cols - 1:
        return False
    return has_word(word[1:], nx, ny, dx, dy)


result = 0
directions = [[dx, dy] for dx in range(-1, 2) for dy in range(-1, 2)]
for x in range(cols):
    for y in range(rows):
        for [dx, dy] in directions:
            result += int(has_word("XMAS", x, y, dx, dy))
print(result)
