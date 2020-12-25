from copy import deepcopy
from itertools import product
from pathlib import Path

EMPTY = 'L'
OCCUPIED = '#'
FLOOR = '.'


def adj(grid, row, col):
    N, M = len(grid), len(grid[0])
    dirs = (-1, 1, 0)
    occupied = 0
    for dx, dy in product(dirs, dirs):
        nrow, ncol = row+dy, col+dx
        if not (dx == 0 and dy == 0) and 0 <= nrow < N and 0 <= ncol < M and grid[nrow][ncol] == OCCUPIED:
            occupied += 1
    return occupied


def adj2(grid, row, col):
    N, M = len(grid), len(grid[0])
    dirs = (-1, 1, 0)
    occupied = 0
    for dx, dy in product(dirs, dirs):
        if dx == 0 and dy == 0:
            continue
        nrow, ncol = row+dy, col+dx
        while 0 <= nrow < N and 0 <= ncol < M:
            if grid[nrow][ncol] != FLOOR:
                if grid[nrow][ncol] == OCCUPIED:
                    occupied += 1
                break
            nrow, ncol = nrow+dy, ncol+dx
    return occupied


def part1(grid):
    N, M = len(grid), len(grid[0])
    changed = True
    while changed:
        aux_grid = deepcopy(grid)
        changed = False
        for row in range(N):
            for col in range(M):
                tile = grid[row][col]
                if tile == FLOOR:
                    continue
                occupied = adj(grid, row, col)
                if tile == EMPTY and occupied == 0:
                    aux_grid[row][col], changed = OCCUPIED, True
                elif tile == OCCUPIED and occupied >= 4:
                    aux_grid[row][col], changed = EMPTY, True
        grid = aux_grid
    total_occ = sum(sum(x == OCCUPIED for x in row) for row in grid)
    return total_occ


def part2(grid):
    N, M = len(grid), len(grid[0])
    changed = True
    while changed:
        aux_grid = deepcopy(grid)
        changed = False
        for row in range(N):
            for col in range(M):
                tile = grid[row][col]
                if tile == FLOOR:
                    continue
                occupied = adj2(grid, row, col)
                if tile == EMPTY and occupied == 0:
                    aux_grid[row][col], changed = OCCUPIED, True
                elif tile == OCCUPIED and occupied >= 5:
                    aux_grid[row][col], changed = EMPTY, True
        grid = aux_grid
    total_occ = sum(sum(x == OCCUPIED for x in row) for row in grid)
    return total_occ


def process_input(file):
    return [list(line) for line in file.read().splitlines()]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        grid = process_input(f)
    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))
