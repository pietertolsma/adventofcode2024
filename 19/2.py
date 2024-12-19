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


mem = {}


def match(remaining):
    if remaining in mem:
        return mem[remaining]
    if len(remaining) == 0:
        return 1
    res = 0
    for size, index in sizes:
        if size > len(remaining):
            return res

        el = elements[index]
        if remaining[:size] != el:
            continue
        check = match(remaining[size:])

        res += check
    mem[remaining] = res
    return res


count = 0
for pattern in patterns:
    res = match(pattern)
    count += res
print(count)
