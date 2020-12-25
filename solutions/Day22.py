from collections import deque
from pathlib import Path


def part1(player1, player2):
    def game(queue1, queue2):
        while len(queue1) > 0 and len(queue2) > 0:
            num1, num2 = queue1.popleft(), queue2.popleft()
            if num1 > num2:
                queue1.extend([num1, num2])
            else:
                queue2.extend([num2, num1])
        return queue1, queue2

    queue1, queue2 = game(deque(player1), deque(player2))

    winner = queue1
    if len(queue2) > 0:
        winner = queue2

    ans = 0
    for i, num in enumerate(reversed(winner)):
        ans += num*(i+1)
    return ans


def part2(player1, player2):
    def game(queue1, queue2):
        store = set()
        while len(queue1) > 0 and len(queue2) > 0:
            key1, key2 = tuple(queue1), tuple(queue2)
            if key1 in store and key2 in store:
                return queue1, deque()
            store.update([key1, key2])

            num1, num2 = queue1.popleft(), queue2.popleft()
            win1 = num1 > num2

            if num1 <= len(queue1) and num2 <= len(queue2):
                q1, q2 = game(deque(list(queue1)[:num1]), deque(
                    list(queue2)[:num2]))
                win1 = len(q1) > len(q2)
            if win1:
                queue1.extend([num1, num2])
            else:
                queue2.extend([num2, num1])
        return queue1, queue2

    queue1, queue2 = game(deque(player1), deque(player2))
    winner = queue1

    if len(queue2) > 0:
        winner = queue2

    ans = 0
    for i, num in enumerate(reversed(winner)):
        ans += num*(i+1)
    return ans


def process_input(file):
    players = file.read().split('\n\n')
    player1 = [int(num) for num in players[0].splitlines()[1:]]
    player2 = [int(num) for num in players[1].splitlines()[1:]]
    return player1, player2


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        player1, player2 = process_input(f)
    print("Part 1:", part1(player1, player2))
    print("Part 2:", part2(player1, player2))
