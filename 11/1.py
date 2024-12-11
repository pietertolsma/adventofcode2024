data = []
with open("data.txt", "r") as file:
    data = [int(el) for el in list(file.readlines()[0].strip().split(" "))]


def split_num(num):
    snum = f"{num}"
    size = len(snum) // 2
    return [int(snum[:size]), int(snum[size:])]


def simulate_step(line):
    new_line = []
    for num in line:
        if num == 0:
            new_line.append(1)
        elif len(f"{num}") % 2 == 0:
            split_nums = split_num(num)
            new_line.append(split_nums[0])
            new_line.append(split_nums[1])
        else:
            new_line.append(num * 2024)
    return new_line


for i in range(25):
    data = simulate_step(data)
print(len(data))
