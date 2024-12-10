from collections import defaultdict

dependencies = defaultdict(list)
updates = []

with open("data.txt", "r") as file:
    init_mode = True
    for line in file.readlines():
        sline = line.strip()
        if sline == "":
            init_mode = False
            continue
        if init_mode:
            [a, b] = sline.split("|")
            dependencies[b].append(a)
        else:
            updates.append(sline.split(","))

count = 0
for update in updates:
    valid = True

    elements = set(update)

    for i in range(len(update)):
        cur = update[i]
        deps = set(dependencies[cur]) & elements
        if not deps.issubset(set(update[: i + 1])):
            valid = False
            break
    if valid:
        middle = len(update) // 2
        count += int(update[middle])
        print("Yes")
print(count)
