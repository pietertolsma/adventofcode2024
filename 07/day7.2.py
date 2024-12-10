import time

data = []
with open("data.txt", "r") as file:
    for line in file.readlines():
        line = line.strip()
        target = line.split(":")[0]
        els = line.split(":")[1].split(" ")[1:]
        data.append([int(el) for el in [target] + els])


def concatenate(a, b):
    return int(f"{a}{b}")


def check_sum(target, elements, cur):
    if len(elements) == 0:
        if cur == target:
            return True
        return False

    a = check_sum(target, elements[1:], cur * elements[0])
    if a:
        return True
    b = check_sum(target, elements[1:], cur + elements[0])
    if b:
        return True

    concat = concatenate(cur, elements[0])
    return check_sum(target, elements[1:], concat)


res = 0
start_time = time.time()
for dat in data:
    if check_sum(dat[0], dat[2:], dat[1]):
        res += dat[0]
print(res)
print("--- %s seconds ---" % (time.time() - start_time))
