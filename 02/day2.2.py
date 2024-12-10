from typing import List


safe_cnts = 0


def is_safe_original(nums):
    if len(nums) <= 1:
        return True

    increasing = int(nums[1]) > int(nums[0])
    for i in range(1, len(nums)):
        prev, cur = int(nums[i - 1]), int(nums[i])
        diff = cur - prev
        if abs(diff) < 1 or abs(diff) > 3:
            return False

        if (increasing and diff < 0) or (not increasing and diff > 0):
            return False
    return True


def is_safe(nums: List[str]) -> bool:
    safe = is_safe_original(nums)
    if not safe:
        for i in range(len(nums)):
            if is_safe_original(nums[:i] + nums[i + 1 :]):
                return True
        return False
    return True


with open("data.txt", "r") as file:
    for line in file:
        res = line.strip().split(" ")
        safe_cnts += 1 if is_safe(res) else 0

print(safe_cnts)
