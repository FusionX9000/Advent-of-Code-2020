import re
from pathlib import Path


def part1(instructions):
    def apply_mask(value, mask):
        ans = 0
        for i, bit in enumerate(reversed(mask)):
            if bit == 'X':
                ans |= value & (1 << i)
            else:
                ans |= int(bit) << i
        return ans

    memory = dict()
    mask = None

    for instruction in instructions:
        if instruction["type"] == "mask":
            mask = instruction["value"]
        else:
            address, value = instruction["value"]
            memory[address] = apply_mask(value, mask)

    return sum(v for v in memory.values())


def part2(instructions):
    """
    Works because input seems to be designed that way. Plenty of scope for optimization 
    but worst case time complexity will remain the same.
    """
    def apply_mask(value, mask, index=0):
        if index >= len(mask):
            yield value
        elif mask[index] == "X":
            yield from apply_mask(value ^ (1 << index), mask, index+1)
            yield from apply_mask(value, mask, index+1)
        else:
            yield from apply_mask(value | (int(
                mask[index]) << index), mask, index+1)

    memory = dict()
    mask = None

    for instruction in instructions:
        if instruction["type"] == "mask":
            mask = instruction["value"]
        else:
            address, value = instruction["value"]
            for fluc_address in apply_mask(address, mask[::-1]):
                memory[fluc_address] = value

    return sum(v for v in memory.values())


def process_input(file):
    instructions = list()
    for line in file.read().splitlines():
        value = line.split('=')[1].strip()
        if line.startswith("mask"):
            instructions.append({"type": "mask", "value": value})
        else:
            address = int(re.search(r'\[(\d+)\]', line).group(1))
            instructions.append(
                {"type": "mem", "value": (address, int(value))})
    return instructions


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        instructions = process_input(f)
    print("Part 1:", part1(instructions))
    print("Part 2:", part2(instructions))
