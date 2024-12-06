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


def is_valid(sequence):
    elements = set(sequence)

    for i in range(len(sequence)):
        cur = sequence[i]
        deps = set(dependencies[cur]) & elements
        if not deps.issubset(set(update[: i + 1])):
            return False
    return True


invalid_updates = []
for update in updates:
    valid = True

    if not is_valid(update):
        invalid_updates.append(update)
        # middle = len(update) // 2
        # count += int(update[middle])


def fix(update):
    for i in range(len(update)):
        cur = update[i]
        deps = set(dependencies[cur])
        invalid_chars = []
        valid_chars = []
        for c in update[i + 1 :]:
            if c in deps:
                invalid_chars.append(c)
            else:
                valid_chars.append(c)
        if len(invalid_chars) > 0:
            return update[:i] + invalid_chars + [cur] + valid_chars
        # find the indices of all chars that are violating
    print("Nothing wrong")
    return update


result = 0
for update in invalid_updates:
    print(update)
    work = fix(update)
    print(work)
    while not is_valid(work):
        work2 = fix(work)
        if work2 == work:
            break
        work = work2
        print(work)
    middle = len(work) // 2
    result += int(work[middle])
print(result)


# 5: [4, 2, 6]
# 4: [2, 1, 6]

# 5 4 3 3 1 How to correct?
