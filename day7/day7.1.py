data = []
with open("data.txt", "r") as file:
    for line in file.readlines():
        line = line.strip()
        target = line.split(":")[0]
        els = line.split(":")[1].split(" ")[1:]
        data.append([int(el) for el in [target] + els])


def check_sum(target, elements):
    if len(elements) == 1:
        if elements[0] == target:
            return True
        return False

    a = check_sum(target / elements[-1], elements[:-1])
    b = check_sum(target - elements[-1], elements[:-1])

    return a or b


res = 0
for dat in data:
    if check_sum(dat[0], dat[1:]):
        print(dat)
        res += dat[0]
print(res)
