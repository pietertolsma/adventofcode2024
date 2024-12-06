import re

res = 0
with open("data.txt", "r") as file:
    enabled = True
    for line in file.readlines():
        pattern = r"(mul\(\d+,\s*\d+\)|do\(\)|don't\(\))"  # Combined regex pattern
        matches = re.findall(pattern, line)
        print(matches)
        for match in matches:
            if match == "do()":
                enabled = True
            elif match == "don't()":
                enabled = False
            else:
                if not enabled:
                    continue
                numspart = match[4:].split(")")[0].split(",")
                res += int(numspart[0]) * int(numspart[1])
print(res)
