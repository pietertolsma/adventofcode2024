from typing import List


safe_cnts = 0


def is_safe(nums: List[str]) -> bool:
    if len(nums) <= 1:
        return True

    increasing = int(nums[1]) > int(nums[0])
    for i in range(1, len(nums)):
        prev, cur = int(nums[i - 1]), int(nums[i])
        diff = cur - prev
        if abs(diff) < 1 or abs(diff) > 3:
            return False
        if increasing and diff < 0:
            return False
        if not increasing and diff > 0:
            return False
    return True


with open("data.txt", "r") as file:
    for line in file:
        res = line.strip().split(" ")
        safe_cnts += 1 if is_safe(res) else 0

print(safe_cnts)
