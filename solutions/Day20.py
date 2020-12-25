from collections import defaultdict
from copy import deepcopy
from enum import Enum, auto

# Lots of scope for improvement in terms of:
# 1. Time complexity - from O(N^2) to O(N) where N is number of tiles
# 2. Object oriented code - this is a great exercise for implementing OOPS principles
# Right now, the code is pretty..sphagetti. Plan to revisit this problem some day and improve the code.
from pathlib import Path


class Side(Enum):
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT = auto()

    @classmethod
    def compare(cls, side1: 'Side', side2: 'Side'):
        if side1 == Side.TOP and side2 == Side.LEFT:
            return 1
        elif side1 == Side.LEFT and side2 == Side.TOP:
            return -1
        return side1.value - side2.value

    def compare_to(self, side2):
        return Side.compare(self, side2)

    def inverse(self):
        total = len(Side)
        return Side(((self.value - 1 + total // 2) % total) + 1)


def get_sides(tile: list[list[str]]) -> tuple['Side', str]:
    for side in Side:
        yield side, get_side(tile, side)


def flip(tile: list[list[str]], side: Side) -> list[list[str]]:
    R, C = len(tile), len(tile[0])
    grid = [[str() for _ in range(C)] for _ in range(R)]
    for r in range(R):
        for c in range(C):
            if side in (Side.TOP, Side.BOTTOM):
                grid[r][c] = tile[r][C - c - 1]
            if side in (Side.RIGHT, Side.LEFT):
                grid[r][c] = tile[R - r - 1][c]
    return grid


def rotate_side(tile: list[list[str]], from_: Side, to: Side) -> list[list[str]]:
    if from_ == to:
        return tile

    R, C = len(tile), len(tile[0])
    grid = [[str() for _ in range(C)] for _ in range(R)]

    diff = from_.compare_to(to)

    for r in range(R):
        for c in range(C):
            if abs(diff) == 2:
                grid[r][c] = tile[R - r - 1][C - c - 1]
            elif diff < 0:
                grid[r][c] = tile[C - c - 1][r]
            elif diff > 0:
                grid[r][c] = tile[c][R - r - 1]
    return grid


def get_side(tile: list[list[str]], side: Side) -> str:
    if side == Side.TOP:
        return "".join(tile[0])
    if side == Side.BOTTOM:
        return "".join(tile[-1])
    if side == Side.LEFT:
        return "".join([t[0] for t in tile])
    if side == Side.RIGHT:
        return "".join([t[-1] for t in tile])


def dfs(tileid_1: int, tiles: dict[int, list[list[str]]], graph: defaultdict[int, dict[int, int]],
        visited: set[int]) -> None:
    if tileid_1 in visited:
        return
    visited.add(tileid_1)

    for tileid_2, tile_2 in tiles.items():
        if tileid_2 == tileid_1:
            continue

        for side_1, val_1 in get_sides(tiles[tileid_1]):
            for side_2, val_2 in get_sides(tile_2):
                if val_1 == val_2 or val_1 == val_2[::-1]:
                    nside = side_1.inverse()
                    ntile = rotate_side(tile_2, side_2, nside)

                    if val_1 != get_side(ntile, nside):
                        ntile = flip(ntile, nside)

                    tiles[tileid_2] = ntile
                    graph[tileid_1][side_1] = tileid_2

    for side, tileid in graph[tileid_1].items():
        dfs(tileid, tiles, graph, visited)


def sort_tiles(tiles: dict[int, list[list[str]]]) -> list[list[int]]:
    graph = defaultdict(dict)

    dfs(list(tiles.keys())[0], tiles, graph, set())

    topleft = [tileid for tileid,
                          val in graph.items() if (Side.LEFT not in val and Side.TOP not in val)][0]

    order = []
    row_start = topleft

    while row_start is not None:
        order.append(list())
        order[-1].append(row_start)

        prev = row_start
        while Side.RIGHT in graph[prev]:
            order[-1].append(graph[prev][Side.RIGHT])
            prev = graph[prev][Side.RIGHT]

        row_start = graph[row_start][Side.BOTTOM] if Side.BOTTOM in graph[row_start] else None

    return order


def part1(tiles: dict[int, list[list[str]]]) -> int:
    order = sort_tiles(tiles)
    return order[0][0] * order[0][-1] * order[-1][0] * order[-1][-1]


def part2(tiles: dict[int, list[list[str]]], dragon: list[list[str]]) -> int:
    def remove_sides(tile: list[list[str]]) -> None:
        tile.pop(0)
        tile.pop(-1)
        for row in tile:
            row.pop(0)
            row.pop(-1)

    def permutations(image: list[list[str]]):
        R, C = len(image), len(image[0])
        grid = deepcopy(image)
        for _ in range(4):

            ngrid = [[str() for _ in range(C)] for _ in range(R)]
            for r in range(R):
                for c in range(C):
                    ngrid[r][c] = grid[c][R - r - 1]
            yield ngrid

            fgrid = [[str() for _ in range(C)] for _ in range(R)]
            for r in range(R):
                for c in range(C):
                    fgrid[r][c] = ngrid[r][C - c - 1]
            yield fgrid
            grid = ngrid

    order = sort_tiles(tiles)
    raw_image = [[tiles[tileid] for tileid in row] for row in order]

    for row in raw_image:
        for tile in row:
            remove_sides(tile)

    image = list()
    for i, row in enumerate(raw_image):
        tile_height = len(row[0])
        nrow: list[list[str]] = [list() for i in range(tile_height)]
        for tile_row_idx in range(tile_height):
            for tile in row:
                nrow[tile_row_idx].extend(tile[tile_row_idx])
        # raw_image[i] = nrow
        image.extend(nrow)

    # for row in raw_image:

    R, C = len(image), len(image[0])
    DR, DC = len(dragon), len(dragon[0])

    def match(x: int, y: int, image: list[list[str]], dragon: list[list[str]]):
        for tx in range(DC):
            for ty in range(DR):
                if dragon[ty][tx] == "#" and image[ty + y][tx + x] != "#":
                    return False
        return True

    for ximage in permutations(image):
        found = False
        for x in range(0, C - DC + 1):
            for y in range(0, R - DR + 1):
                if match(x, y, ximage, dragon):
                    found = True
                    for tx in range(DC):
                        for ty in range(DR):
                            if dragon[ty][tx] == "#":
                                ximage[ty + y][tx + x] = 'X'
        if found:
            return sum(sum(char == '#' for char in row) for row in ximage)


def process_input(file):
    raw_tiles = file.read().split('\n\n')
    tiles = dict()
    for raw_tile in raw_tiles:
        raw_tile = raw_tile.splitlines()
        tile_id = int(raw_tile[0].split()[1].replace(':', ''))
        tile = raw_tile[1:]
        tiles[tile_id] = [list(row) for row in tile]
    return tiles


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        tiles = process_input(f)
    print("Part 1:", part1(tiles))

    with open('../inputs/dragon.txt', 'r') as f:
        dragon = [list(r) for r in f.read().splitlines()]
    print("Part 2:", part2(tiles, dragon))
