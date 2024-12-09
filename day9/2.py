from time import time


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

empty_pointer, left_trailing_pointer, trailing_pointer = (
    0,
    len(layout) - 1,
    len(layout) - 1,
)


def search_and_insert(start, end, symbol, length):
    left, right = start, start
    while right < end and (right - left) < length:
        if layout[right] != ".":
            left, right = right + 1, right + 1
        else:
            right += 1
    # Check if we found a gap
    if right - left == length:
        for left in range(left, left + length):
            layout[left] = symbol
        return True
    return False


start_time = time()
while empty_pointer < trailing_pointer:
    if layout[empty_pointer] != ".":
        empty_pointer += 1
        continue
    if layout[trailing_pointer] == ".":
        trailing_pointer -= 1
        continue

    while (
        left_trailing_pointer > trailing_pointer
        or layout[left_trailing_pointer - 1] == layout[trailing_pointer]
    ):
        left_trailing_pointer -= 1
        continue

    target_length = trailing_pointer - left_trailing_pointer + 1
    if search_and_insert(
        empty_pointer,
        left_trailing_pointer,
        layout[left_trailing_pointer],
        target_length,
    ):
        for l in range(left_trailing_pointer, left_trailing_pointer + target_length):
            layout[l] = "."
    trailing_pointer = left_trailing_pointer - 1


score = 0
for i, num in enumerate(layout):
    if num == ".":
        continue
    score += i * num

print(score)
print("--- %s seconds ---" % (time() - start_time))
