from functools import reduce


def part1(groups):
    return reduce(lambda count, group: count + len(set.union(*map(set, group))), groups, 0)


def part2(groups):
    return reduce(lambda count, group: count + len(set.intersection(*map(set, group))), groups, 0)


def process_input(file):
    return [[answers for answers in group.split('\n')] for group in file.read().split('\n\n')]


if __name__ == "__main__":
    with open('../inputs/Day6.txt', 'r') as f:
        groups = process_input(f)
    print("Part 1:", part1(groups))
    print("Part 2:", part2(groups))
