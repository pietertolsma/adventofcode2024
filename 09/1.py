raw_data = []
with open("data.txt", "r") as f:
    raw_data = list(f.readlines()[0].strip())

layout = []
for i in range(len(raw_data)):
    symbol = "."
    if i % 2 == 0:
        symbol = i // 2
    for j in range(int(raw_data[i])):
        layout.append(symbol)

empty_pointer, trailing_pointer = 0, len(layout) - 1

while empty_pointer < trailing_pointer:
    if layout[empty_pointer] != ".":
        empty_pointer += 1
        continue
    if layout[trailing_pointer] == ".":
        trailing_pointer -= 1
        continue

    layout[empty_pointer] = layout[trailing_pointer]
    layout[trailing_pointer] = "."
    empty_pointer += 1
    trailing_pointer -= 1


score = 0
for i, num in enumerate(layout[: trailing_pointer + 1]):
    if num == ".":
        continue
    score += i * num

print(score)
