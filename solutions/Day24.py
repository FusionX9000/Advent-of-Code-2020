from collections import defaultdict
from io import TextIOWrapper
from pathlib import Path

step = {
    'w': lambda x, y: (x-2, y),
    'e': lambda x, y: (x+2, y),
    'ne': lambda x, y: (x+1, y+1),
    'nw': lambda x, y: (x-1, y+1),
    'se': lambda x, y: (x+1, y-1),
    'sw': lambda x, y: (x-1, y-1),
}

# Same as day 17
# For part 1, use a map to save states of the tile for part 1 and do as asked.
# For part 2, this is the 3rd (or fourth? I've lost count) puzzle on Cellular automaton similar to Conway's game of life
# We only care about black tiles and so save their states in a set for each day and update simultaneously.


def prepare_tiles(instructions: list[list[str]]) -> defaultdict[tuple[int, int], int]:
    tiles = defaultdict(int)
    for instruction in instructions:
        x = y = 0
        for direction in instruction:
            x, y = step[direction](x, y)
        tiles[(x, y)] ^= 1
    return tiles


def part1(instructions: list[list[str]]) -> int:
    return sum(val == 1 for val in prepare_tiles(instructions).values())


def part2(instructions: list[list[str]]) -> int:
    tiles = prepare_tiles(instructions)
    black_tiles = set([k for k, v in tiles.items() if v == 1])

    for day in range(100):
        new_black_tiles = set()
        adj_count = defaultdict(int)

        for (x, y) in black_tiles:
            for nei_fnc in step.values():
                adj_count[nei_fnc(x, y)] += 1

        for coord, count in adj_count.items():
            if (coord in black_tiles and 1 <= count <= 2) or count == 2:
                new_black_tiles.add(coord)
        black_tiles = new_black_tiles

    return len(black_tiles)


def process_input(file: TextIOWrapper) -> list[list[str]]:
    instructions = list()
    for line in file.read().splitlines():
        instruction = list()
        i = 0
        while i < len(line):
            if line[i].startswith('n') or line[i].startswith('s'):
                char = line[i:i+2]
                i += 2
            else:
                char = line[i]
                i += 1
            instruction.append(char)
        instructions.append(instruction)
    return instructions


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        instructions = process_input(f)
    print("Part 1:", part1(instructions))
    print("Part 2:", part2(instructions))
