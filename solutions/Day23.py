from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path


@dataclass
class ListNode:
    val: int
    next: 'ListNode' = None

# Possible optimization as suggested by some people in /r/adventofcode
# Since the number of labels is N and range of is between 1 and N, and we can use an array as map, instead of a linked list


def crab_cups(labels: list[int], max_labels: int, moves: int) -> ListNode:
    N = len(labels)

    start = ListNode(0)
    node = start

    num_map: dict[int, ListNode] = dict()

    for i in range(max_labels):
        num = i+1
        if i < N:
            num = labels[i]

        new_node = ListNode(num)
        num_map[num] = new_node
        node.next = new_node
        node = node.next

    node.next = start.next
    current_cup = start.next

    for move in range(moves):
        if move % 100000 == 0:
            print(move)

        pickedup_cups = set()
        cons_cups_end = cons_cups_start = current_cup.next
        for _ in range(3-1):
            pickedup_cups.add(cons_cups_end.val)
            cons_cups_end = cons_cups_end.next
        pickedup_cups.add(cons_cups_end.val)

        current_cup.next = cons_cups_end.next
        cons_cups_end.next = None

        dest_cup = current_cup.val-1
        while dest_cup in pickedup_cups or dest_cup < 1:
            if dest_cup < 1:
                dest_cup = max_labels
            else:
                dest_cup -= 1

        dest_cup_node = num_map[dest_cup]
        cons_cups_end.next = dest_cup_node.next
        dest_cup_node.next = cons_cups_start

        current_cup = current_cup.next

    return num_map[1]


def part1(labels: list[int]) -> int:
    N = len(labels)
    res = list()

    node = crab_cups(labels, N, 100).next
    while node.val != 1:
        res.append(node.val)
        node = node.next

    return "".join(list(map(str, res)))


def part2(labels: list[int]) -> int:
    node = crab_cups(labels, 10**6, 10**7)
    return node.next.val*node.next.next.val


def process_input(file: TextIOWrapper) -> list[int]:
    return [int(num) for num in file.read()]


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    input_path = script_path.parent / '../inputs' / f'{script_path.stem}.txt'

    with input_path.open('r') as f:
        labels = process_input(f)
    print("Part 1:", part1(labels))
    print("Part 2:", part2(labels))
