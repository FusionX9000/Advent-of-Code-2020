from pathlib import Path


def part1(instructions):
    # Using boolean array instead of set since range is known and fixed
    visited = [False]*len(instructions)
    line = 0
    value = 0

    while line < len(instructions) and not visited[line]:
        visited[line] = True
        opn, arg = instructions[line]
        if opn == 'acc':
            value += arg
        if opn == 'jmp':
            line += arg
        else:
            line += 1
    return value


def part2_optimized(instructions):
    """ 
    Code could be cleaner but it's O(N) instead of O(N^2). 
    The trick is to notice that that lines which previously led to a loop (before and after modification),
    will always lead to a loop. So we keep track of these lines and backtrack when its visited again (memoization). 
    """
    visited = [False]*len(instructions)

    def f(line, flip):
        if line >= len(instructions):
            return 0
        if visited[line]:
            return None

        visited[line] = True
        res = None
        opn, arg = instructions[line]

        if opn == 'acc':
            if (next_ := f(line + 1, flip)) is not None:
                res = next_ + arg
        elif opn == 'jmp':
            res = f(line+arg, flip)
            if res is None and not flip:
                res = f(line+1, True)
        else:  # nop
            res = f(line+1, flip)
            if res is None and not flip:
                res = f(line+arg, True)
        return res
    return f(0, False)


def part2(instructions):
    """
    O(N^2), simple extension from part 1 solution. We make no assumption here and end up doing redudnant work
    """
    def run():
        visited = [False]*len(instructions)
        line = 0
        value = 0

        while line < len(instructions):
            if visited[line]:
                return False
            visited[line] = True
            opn, arg = instructions[line]
            if opn == 'acc':
                value += arg
            if opn == 'jmp':
                line += arg
            else:
                line += 1
        return value

    for line, instruction in enumerate(instructions):
        opn, arg = instruction
        if opn == 'acc':
            continue
        if opn == 'jmp':
            instructions[line] = ('nop', arg)
        elif opn == 'nop':
            instructions[line] = ('jmp', arg)
        value = run()
        if value:
            return value
        instructions[line] = (opn, arg)


def process_input(file):
    return [(opn, int(arg)) for opn, arg in [line.split() for line in file.read().splitlines()]]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        instructions = process_input(f)
    print("Part 1:", part1(instructions))
    print("Part 2:", part2(instructions))
    print("Part 2 optimized:", part2_optimized(instructions))
