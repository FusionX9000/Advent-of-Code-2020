from functools import reduce
from pathlib import Path


def part1(start, ids):
    ids = [id_ for id_ in ids if id_ != "x"]
    res_id = min_time = None
    for _, id_ in enumerate(ids):
        wait_time = id_ - (start % id_)
        if min_time is None or wait_time < min_time:
            res_id, min_time = id_, wait_time
    return res_id*min_time


def part2(ids):
    def extended_euclidean(a, b):
        if b == 0:
            x, y = 1, 0
            return a, x, y
        d, x1, y1 = extended_euclidean(b, a % b)
        x, y = y1, x1-y1 * (a//b)
        return d, x, y

    def mod_inverse(a, m):
        _g, x, _y = extended_euclidean(a, m)
        return (x % m+m) % m

    pairs = [(-i, id_)
             for i, id_ in enumerate(ids) if id_ != "x"]
    N = reduce(lambda a, x: a*x, [m for a, m in pairs], 1)
    Ni = [N//m for a, m in pairs]
    Mi = [mod_inverse(N//m, m) for a, m in pairs]
    ans = sum(Ni[i]*Mi[i]*pairs[i][0] for i in range(len(pairs)))
    return ans % N


def process_input(file):
    start = int(file.readline().strip())
    return start, [int(id_.strip()) if id_ != "x" else id_ for id_ in file.read().split(',')]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        start, ids = process_input(f)
    print("Part 1:", part1(start, ids))
    print("Part 2:", part2(ids))
