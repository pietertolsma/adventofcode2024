a = []
b = []
with open("data.txt", "r") as file:
    for line in file:
        res = line.strip().split(" ")
        a.append(res[0])
        b.append(res[3])

a.sort()
b.sort()

dist = 0
for [elA, elB] in zip(a, b):
    dist += abs(int(elA) - int(elB))
print(dist)
