import math

y = (1, 0, -1, 0)
x = (0, 1, 0, -1)

dirs = ('N', 'E', 'S', 'W')
dirs_coord = dict(zip(dirs, zip(x, y)))


def part1(sequence):
    cx = cy = 0
    curr_dir = dirs.index('E')
    for action, value in sequence:
        if action in dirs_coord:
            dx, dy = dirs_coord[action]
            cx, cy = cx+(dx*value), cy+(dy*value)
        elif action == 'F':
            dx, dy = dirs_coord[dirs[curr_dir]]
            cx, cy = cx+(dx*value), cy+(dy*value)
        else:
            sign = 1 if action == 'R' else -1
            move = (value//90)
            curr_dir = (curr_dir+(sign*move)) % len(dirs)

    return abs(cx)+abs(cy)


def part2(sequence):

    def rotate(point, angle):
        angle = math.radians(angle)
        (px, py) = point
        px_ = (px)*math.cos(angle) - (py)*math.sin(angle)
        py_ = (py)*math.cos(angle) + (px)*math.sin(angle)
        return round(px_), round(py_)

    cx = cy = 0
    wx, wy = 10, 1

    for action, value in sequence:
        if action in dirs_coord:
            dx, dy = dirs_coord[action]
            wx, wy = wx+(dx*value), wy+(dy*value)
        elif action == 'F':
            cx, cy = cx+(wx*value), cy+(wy*value)
        else:
            sign = -1 if action == 'R' else 1
            wx, wy = rotate((wx, wy), sign*value)
        print(action+str(value), f'({cx},{cy})',
              f'({wx},{wy})')

    return abs(cx)+abs(cy)


def process_input(file):
    return [(x[0], int(x[1:])) for x in file.read().splitlines()]


if __name__ == "__main__":
    with open('../inputs/Day12.txt', 'r') as f:
        sequence = process_input(f)
    print("Part 1:", part1(sequence))
    print("Part 2:", part2(sequence))
    print(part2([("L", 270)]))
