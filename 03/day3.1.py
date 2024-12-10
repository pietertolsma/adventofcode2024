import re

res = 0
with open("data.txt", "r") as file:
    for line in file.readlines():
        pattern = r"mul\(\d+,\s*\d+\)"  # Regex pattern
        matches = re.findall(pattern, line)
        for match in matches:
            numspart = match[4:].split(")")[0].split(",")
            res += int(numspart[0]) * int(numspart[1])
print(res)
