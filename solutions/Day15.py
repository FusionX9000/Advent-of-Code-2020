def part1(nums):
    index = dict()

    # initialize
    for i in range(len(nums)-1):
        index[nums[i]] = i

    prev = nums[-1]

    for i in range(len(nums), 2020):
        next = 0
        if prev in index:
            next = (i-1)-index[prev]
        index[prev], prev = i-1, next

    return prev


def part2(nums):
    index = dict()

    # initialize
    for i in range(len(nums)-1):
        index[nums[i]] = i

    prev = nums[-1]

    for i in range(len(nums), 30000000):
        next = 0
        if prev in index:
            next = (i-1)-index[prev]
        index[prev], prev = i-1, next

    return prev


def process_input(file):
    return [int(num) for num in file.read().split(',')]


if __name__ == "__main__":
    with open('../inputs/Day15.txt', 'r') as f:
        nums = process_input(f)
    print("Part 1:", part1(nums))
    print("Part 2:", part2(nums))
