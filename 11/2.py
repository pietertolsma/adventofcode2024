from collections import defaultdict
from time import time
from typing import Counter


counts = {}
with open("data.txt", "r") as file:
    data = [int(el) for el in list(file.readlines()[0].strip().split(" "))]
    counts = Counter(data)


def split_num(num):
    snum = f"{num}"
    size = len(snum) // 2
    return [int(snum[:size]), int(snum[size:])]


def simulate_step(data):
    new_counts = defaultdict(int)
    for num, count in data.items():
        if num == 0:
            new_counts[1] += 1 * count
        elif len(f"{num}") % 2 == 0:
            split_nums = split_num(num)
            new_counts[split_nums[0]] += count
            new_counts[split_nums[1]] += count
        else:
            new_counts[num * 2024] += count
    return new_counts


start_time = time()
for i in range(75):
    counts = simulate_step(counts)

res = 0
for num, count in counts.items():
    res += count

print("--- %s seconds ---" % (time() - start_time))
