from pathlib import Path


def decode(code):
    l, r = 0, (1 << len(code))-1
    for ch in code:
        mid = l + (r-l)//2
        if(ch == '0'):
            r = mid
        else:
            l = mid+1
    return l


def calculate_seatid(row_number, col_number):
    return row_number*8+col_number


def part1(seat_codes):
    return max(calculate_seatid(decode(row_code), decode(col_code)) for row_code, col_code in seat_codes)

# We can also use a sorted list, but time complexity will be O(NlogN) instead of O(N)


def part2(seat_codes):
    seatids = set([calculate_seatid(decode(row_code), decode(col_code))
                   for row_code, col_code in seat_codes])
    l, r = min(seatids), max(seatids)
    for seatid in range(l+1, r):
        if seatid not in seatids:
            return seatid
    return -1


def process_input(file):
    def process_code(code):
        code = code.replace('F', '0').replace(
            'L', '0').replace('B', '1').replace('R', '1')
        return code[:-3], code[-3:]

    return [(row_code, col_code) for row_code, col_code in [process_code(line.rstrip()) for line in file]]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        seat_codes = process_input(f)
    print("Part 1:", part1(seat_codes))
    print("Part 2:", part2(seat_codes))
