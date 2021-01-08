from pathlib import Path

MOD = 20201227
SUBJECT_NUM = 7


def part1(keys):
    def transform(subject_num):
        key = 1
        while True:
            key = (key*subject_num) % MOD
            yield key

    pbk_a, pbk_b = keys
    prk_a = enc_key = 1

    gen = transform(7)
    while pbk_a != next(gen):
        prk_a += 1

    gen = transform(pbk_b)
    for _ in range(prk_a):
        enc_key = next(gen)

    return enc_key


def process_input(file):
    return list(map(int, file.read().splitlines()))


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        keys = process_input(f)
    print("Part 1:", part1(keys))
