data = []
with open("data2.txt", "r") as file:
    for line in file.readlines():
        line = line.strip()
        target = line.split(":")[0]
        els = line.split(":")[1].split(" ")[1:]
        data.append([int(el) for el in [target] + els])


def concatenate(a, b):
    return int(f"{a}{b}")


def check_sum(target, elements):
    if len(elements) == 1:
        if elements[0] == target:
            return True
        return False

    if len(elements) == 0:
        return target == 0

    concat_end = concatenate(elements[-2], elements[-1])
    if len(elements) == 2 and concat_end == target:
        return True

    a = check_sum(target / elements[-1], elements[:-1])
    if a:
        return True
    b = check_sum(target - elements[-1], elements[:-1])
    if b:
        return True

    return check_sum(target - concat_end, elements[:-2])


res = 0
for dat in data:
    if check_sum(dat[0], dat[1:]):
        print(dat)
        res += dat[0]
print(res)
