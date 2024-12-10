from collections import Counter

a = []
b = []
with open("data.txt", "r") as file:
    for line in file:
        res = line.strip().split(" ")
        a.append(res[0])
        b.append(res[3])

b_cnts = Counter(b)
a_items = set(a)

score = 0
for el in a_items:
    score += int(el) * int(b_cnts.get(el, 0))
print(score)
