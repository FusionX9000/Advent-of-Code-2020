from functools import reduce
from pathlib import Path


def traverse_grid(grid, slope):
    x, y = 0, 0
    dx, dy = slope
    end = len(grid)
    ans = 0
    while(y < end):
        ans += 1 if grid[y][x] == '#' else 0
        x = (x+dx) % len(grid[0])
        y += dy
    return ans


def part1(grid):
    slope = (3, 1)
    return traverse_grid(grid, slope)


def part2(grid):
    slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))
    return reduce(lambda a, x: a*x, map(lambda slope: traverse_grid(grid, slope), slopes))


def process_input(input_):
    return input_


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        grid = process_input([line.rstrip() for line in f])
    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))
