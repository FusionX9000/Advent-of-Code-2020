from collections import namedtuple, deque, defaultdict
import re


def part1(parents):
    q = deque(['shiny gold'])
    visited = set()
    while len(q) > 0:
        bag = q.popleft()
        parent_bags = parents[bag]
        visited.update(parent_bags)
        for parent_bag in parent_bags:
            q.append(parent_bag)
    return len(visited)


def part2(rules):
    q = deque(rules['shiny gold'])
    res = 0
    while len(q) > 0:
        count, bag = q.popleft()
        for next_count, next_bag in rules[bag]:
            q.append((count*next_count, next_bag))
        res += count

    return res


def process_input(file):
    parent_pat = re.compile(r'([a-z]+ [a-z]+) bags contain')
    children_pat = re.compile(r'(\d+) ([a-z]+ [a-z]+) bag[s]*')

    rules = dict()
    parents = defaultdict(list)

    for line in file.read().split('\n'):
        parent_bag = re.match(parent_pat, line).group(1)
        contains = re.findall(children_pat, line)

        rules[parent_bag] = [(int(count), bag) for count, bag in contains]

        for count, bag in rules[parent_bag]:
            parents[bag].append(parent_bag)
    return parents, rules


if __name__ == "__main__":
    with open('../inputs/Day7.txt', 'r') as f:
        parents, rules = process_input(f)
    print("Part 1:", part1(parents))
    print("Part 2:", part2(rules))
