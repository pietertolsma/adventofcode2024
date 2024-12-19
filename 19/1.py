input_file = "data.txt"
elements = []
patterns = []

with open(input_file, "r") as file:
    elements = file.readline().strip().split(", ")
    file.readline()
    for line in file.readlines():
        patterns.append(line.strip())

# Dynamic programming, sliding window


sizes = sorted([(len(el), i) for i, el in enumerate(elements)])


def match(remaining):
    if len(remaining) == 0:
        return True
    for size, index in sizes:
        if size > len(remaining):
            return False

        el = elements[index]
        if remaining[:size] != el:
            continue
        if match(remaining[size:]):
            return True
    return False


count = 0
for pattern in patterns:
    if match(pattern):
        count += 1
print(count)
