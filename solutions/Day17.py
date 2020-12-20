from copy import deepcopy
from itertools import product
from collections import defaultdict

ACTIVE = "#"
INACTIVE = "."


def get_range(space):
    res = list()
    while space and isinstance(space, list):
        res.append(len(space))
        space = space[0]
    return reversed(res)


def neighbors(coord):
    dirs = (-1, 0, 1)
    count_dims = len(coord)
    for dd in product(*[dirs for _ in range(count_dims)]):
        if all(ddi == 0 for ddi in dd):
            continue
        nd = tuple([coord[i]+dd[i] for i in range(count_dims)])
        yield nd


def play(active):
    inactive_map = defaultdict(int)
    next_active = set()

    for cube in active:
        count = 0
        for nei in neighbors(cube):
            if nei in active:
                count += 1

            inactive_map[nei] += 1

        if 2 <= count <= 3:
            next_active.add(cube)

    for cube, active_nei_count in inactive_map.items():
        if active_nei_count == 3:
            next_active.add(cube)

    return next_active


def part1(grid):
    X, Y = get_range(grid)

    active = set()

    for x in range(X):
        for y in range(Y):
            if grid[x][y] == ACTIVE:
                active.add((x, y, 0))

    for _ in range(6):
        active = play(active)
    return len(active)


def part2(grid):
    X, Y = get_range(grid)

    active = set()

    for x in range(X):
        for y in range(Y):
            if grid[x][y] == ACTIVE:
                active.add((x, y, 0, 0))

    for _ in range(6):
        active = play(active)
    return len(active)


def process_input(file):
    return [list(line) for line in file.read().splitlines()]


if __name__ == "__main__":
    with open('../inputs/Day17.txt', 'r') as f:
        grid = process_input(f)
    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))
