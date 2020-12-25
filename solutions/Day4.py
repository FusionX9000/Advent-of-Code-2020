import re
from functools import reduce
from pathlib import Path

# Not safe for work
rules = {
    'byr': lambda x: 1920 <= int(x) <= 2002,
    'iyr': lambda x: 2010 <= int(x) <= 2020,
    'eyr': lambda x: 2020 <= int(x) <= 2030,
    'hgt': lambda x: (x.endswith('cm') and 150 <= int(x[:-2] or 0) <= 193) or (x.endswith('in') and 59 <= int(x[:-2] or 0) <= 76),
    'hcl': lambda x: re.match(r'#[\da-f]{6}$', x) != None,
    'ecl': lambda x: x in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda x: re.match(r'\d{9}$', x) != None,
    'cid': lambda x: True,
}

# Nobody: How unreadable should the code be?
# Me: yes


def part1(passports):
    return reduce(lambda count, passport: count + (1 if len(passport) == 8 or (len(passport) == 7 and 'cid' not in passport) else 0), passports, 0)


def part2(passports):
    def verify(passport):
        return (len(passport) == 8 or (len(passport) == 7 and 'cid' not in passport)) and all(rules[field](value) for field, value in passport.items())
    return reduce(lambda count, passport: count + (1 if verify(passport) else 0), passports, 0)


def process_input(file):
    return [{key: value for key, value in re.findall(r'(\S+):(\S+)', passport_data)} for passport_data in file.read().split('\n\n')]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        passports = process_input(f)
    print("Part 1:", part1(passports))
    print("Part 2:", part2(passports))
