from collections import defaultdict
from pathlib import Path


def part1(nums):
    nums = sorted(nums)
    diff = defaultdict(int)
    diff[nums[0]] = 1
    for i in range(1, len(nums)):
        diff[nums[i]-nums[i-1]] += 1
    return (diff[3]+1)*diff[1]


def part2(nums):
    nums = sorted(nums+[0])
    N = len(nums)
    dp = [0]*N
    dp[N-1] = 1

    for i in reversed(range(N)):
        for j in range(i+1, N):
            if nums[j]-nums[i] > 3:
                break
            dp[i] += dp[j]

    return dp[0]


def process_input(file):
    return [int(num) for num in file.read().splitlines()]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        nums = process_input(f)
    print("Part 1:", part1(nums))
    print("Part 2:", part2(nums))
