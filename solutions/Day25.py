MOD = 20201227
SUBJECT_NUM = 7
# unnecessary since there's already a faster builtin C implementation in CPython.

# def mod_pow(x, n, mod):
#     if mod == 1:
#         return 0
#     res = 1
#     x = x % MOD
#     while(n > 0):
#         if (n % 2) & 1:
#             res = (x*res) % MOD
#         x = (x*x) % MOD
#         n >>= 1
#     return res


def part1(keys):
    pbk_a, pbk_b = keys
    for k in range(2, MOD):
        if pow(SUBJECT_NUM, k, MOD) == pbk_a:
            return pow(pbk_b, k, MOD)


def process_input(file):
    return list(map(int, file.read().splitlines()))


if __name__ == "__main__":
    with open('../inputs/Day25.txt', 'r') as f:
        keys = process_input(f)
    print("Part 1:", part1(keys))