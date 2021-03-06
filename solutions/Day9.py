"""
Plenty of minor optimizations possible for this day's problem but asymptotically time complexity will remain O(N) 
"""
from pathlib import Path


def two_sum(nums, target):
    operands = set()
    for num in nums:
        if num in operands:
            return True
        operands.add(target-num)
    return False


def part1(nums):
    l = 0
    for r, num in enumerate(nums):
        if (r-l+1) > 25:
            if not two_sum(nums[l:r], num):
                return num
            l += 1
    return None


def part2(nums):
    target = part1(nums)

    l = r = 0
    running_sum = 0
    prefix_sum = dict()

    for r, num in enumerate(nums):
        running_sum += num
        if (sum_ := running_sum - target) in prefix_sum:
            l = prefix_sum[sum_] + 1
            break
        prefix_sum[running_sum] = r
    return min(nums[l:r+1]) + max(nums[l:r+1])


def process_input(file):
    return [int(num) for num in file.read().splitlines()]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        nums = process_input(f)
    print("Part 1:", part1(nums))
    print("Part 2:", part2(nums))
