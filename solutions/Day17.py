from copy import deepcopy
from itertools import product

ACTIVE = "#"
INACTIVE = "."


def get_range(space):
    res = list()
    while space and isinstance(space, list):
        res.append(len(space))
        space = space[0]
    return reversed(res)

# An exercise in pedantry. Only attempt this if you have a God-complex and intend to simulate an infinite universe.
# For mere mortals, its suggsted you create a finite universe big enough to fit our input constraints and let there be light.


def neighbors_1(space, x, y, z):
    X, Y, Z = get_range(space)

    dirs = (-1, 0, 1)

    for dx, dy, dz in product(dirs, dirs, dirs):
        if dx == 0 and dy == 0 and dz == 0:
            continue
        nx, ny, nz = dx+x, dy+y, dz+z
        if 0 <= nx < X and 0 <= ny < Y and 0 <= nz < Z:
            yield nx, ny, nz


def add_layers(space):
    X, Y, Z = get_range(space)

    # top
    ok = False
    for x in range(X):
        for z in range(Z):
            active = 0
            for nx, ny, nz in neighbors_1(space, x, -1, z):
                if space[nz][ny][nx] == ACTIVE:
                    active += 1
                if active == 3:
                    ok = True
                    break
    if ok:
        for z in range(Z):
            layer = list("."*X)
            space[z].insert(0, layer)

    # bottom
    X, Y, Z = get_range(space)

    ok = False
    for x in range(X):
        for z in range(Z):
            active = 0
            for nx, ny, nz in neighbors_1(space, x, Y, z):
                if space[nz][ny][nx] == ACTIVE:
                    active += 1
                if active == 3:
                    ok = True
                    break
    if ok:
        for z in range(Z):
            layer = list("."*X)
            space[z].append(layer)

    # left
    X, Y, Z = get_range(space)

    ok = False
    for y in range(Y):
        for z in range(Z):
            active = 0
            for nx, ny, nz in neighbors_1(space, -1, y, z):
                if space[nz][ny][nx] == ACTIVE:
                    active += 1
                if active == 3:
                    ok = True
                    break
    if ok:
        for z in range(Z):
            for y in range(Y):
                space[z][y].insert(0, ".")

    # right
    X, Y, Z = get_range(space)

    ok = False
    for y in range(Y):
        for z in range(Z):
            active = 0
            for nx, ny, nz in neighbors_1(space, X, y, z):
                if space[nz][ny][nx] == ACTIVE:
                    active += 1
                if active == 3:
                    ok = True
                    break
    if ok:
        for z in range(Z):
            for y in range(Y):
                space[z][y].append(".")

    # front
    X, Y, Z = get_range(space)

    ok = False
    for x in range(X):
        for y in range(Y):
            active = 0
            for nx, ny, nz in neighbors_1(space, x, y, -1):
                if space[nz][ny][nx] == ACTIVE:
                    active += 1
                if active == 3:
                    ok = True
                    break
    if ok:
        space.insert(0, [list("."*X) for y in range(Y)])

    # back
    X, Y, Z = get_range(space)

    ok = False
    for x in range(X):
        for y in range(Y):
            active = 0
            for nx, ny, nz in neighbors_1(space, x, y, Z):
                if space[nz][ny][nx] == ACTIVE:
                    active += 1
                if active == 3:
                    ok = True
                    break
    if ok:
        space.append([list("."*X) for y in range(Y)])


def part1(grid):

    def play(space):
        add_layers(space)
        X, Y, Z = get_range(space)
        cspace = deepcopy(space)

        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    active = 0
                    for nx, ny, nz in neighbors_1(space, x, y, z):
                        if space[nz][ny][nx] == ACTIVE:
                            active += 1
                    if space[z][y][x] == ACTIVE and (active < 2 or active > 3):
                        cspace[z][y][x] = INACTIVE
                    elif space[z][y][x] == INACTIVE and active == 3:
                        cspace[z][y][x] = ACTIVE
        return cspace

    space = [grid]
    for _ in range(6):
        space = play(space)

    X, Y, Z = get_range(space)
    count = 0
    for x in range(X):
        for y in range(Y):
            for z in range(Z):
                if space[z][y][x] == ACTIVE:
                    count += 1

    return count


def create_universe(grid, limit):
    X, Y, Z, W = 2*limit + len(grid[0]), 2 * \
        limit + len(grid), 2*limit+1, 2*limit+1

    space = [[[['.' for x in range(X)] for y in range(Y)]
              for z in range(Z)] for w in range(W)]

    start_x = start_y = limit
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            space[W//2][Z//2][y+start_y][x+start_x] = grid[y][x]
    return space


def part2(grid):
    def neighbors(space, x, y, z, w):
        X, Y, Z, W = get_range(space)
        dirs = (-1, 0, 1)
        for dx, dy, dz, dw in product(dirs, dirs, dirs, dirs):
            if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                continue
            nx, ny, nz, nw = dx+x, dy+y, dz+z, dw+w
            if 0 <= nx < X and 0 <= ny < Y and 0 <= nz < Z and 0 <= nw < W:
                yield nx, ny, nz, nw

    def play(space):
        X, Y, Z, W = get_range(space)
        cspace = deepcopy(space)

        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    for w in range(W):
                        active = 0
                        for nx, ny, nz, nw in neighbors(space, x, y, z, w):
                            if space[nw][nz][ny][nx] == ACTIVE:
                                active += 1
                        if space[w][z][y][x] == ACTIVE and (active < 2 or active > 3):
                            cspace[w][z][y][x] = INACTIVE
                        elif space[w][z][y][x] == INACTIVE and active == 3:
                            cspace[w][z][y][x] = ACTIVE
        return cspace

    # For our sanity, we pretend there's no infinite universe. We take the blue pill.
    space = create_universe(grid, 6)

    for _ in range(6):
        print("round", _)
        space = play(space)

    X, Y, Z, W = get_range(space)
    count = 0
    for x in range(X):
        for y in range(Y):
            for z in range(Z):
                for w in range(W):
                    if space[w][z][y][x] == ACTIVE:
                        count += 1

    return count


def process_input(file):
    return [list(line) for line in file.read().splitlines()]


if __name__ == "__main__":
    with open('../inputs/Day17.txt', 'r') as f:
        grid = process_input(f)
    print("Part 1:", part1(grid))
    print("Part 2:", part2(grid))
