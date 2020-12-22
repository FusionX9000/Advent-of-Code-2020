import regex
import sys
from collections import namedtuple
import re

# We've been given a grammar and have to check if a message belongs to the grammar.
# Solution specific to input constraints only

Result = namedtuple('Result', ['parsed', 'index'])

dp = dict()


def permute(rule_idx, message, index):
    key = (rule_idx, index)
    if key in dp:
        return dp[key]

    ans = list()
    children = rules[rule_idx]

    if index >= len(message):
        return ans

    if len(children) == 1 and isinstance((terminal := children[0][0]), str):
        if message[index] == terminal:
            ans.append(index+1)
    else:
        for nodes in children:
            next_indexes = [index]
            for i, node in enumerate(nodes):
                tmp = []
                for next_idx in next_indexes:
                    results = permute(node, message, next_idx)
                    tmp.extend(results)
                next_indexes = tmp
            ans.extend(next_indexes)

    dp[key] = ans
    return ans


def check(message):
    dp.clear()
    return any(idx == len(message) for idx in permute(0, message, 0))


def part1(rules, messages):
    """ 
    permute function does not really need DP or building an index array for part 1.
    But using a generalized approach makes for an easier time solving part 2.
    """
    return sum(check(message) for message in messages)


def part2(rules, messages):
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    return sum(check(message) for message in messages)


def process_input(file):
    raw_rules, raw_messages = file.read().split('\n\n')
    rules = dict()
    for raw_rule in raw_rules.split('\n'):
        delim = raw_rule.find(':')
        name = raw_rule[:delim]
        children = [[int(x) if x.isnumeric() else x.replace('"', '') for x in y] for y in [z.strip().split()
                                                                                           for z in raw_rule[delim+1:].split(' | ')]]
        rules[int(name)] = children
    messages = raw_messages.strip().splitlines()
    return rules, messages


if __name__ == "__main__":
    with open('../inputs/Day19.txt', 'r') as f:
        rules, messages = process_input(f)
    print("Part 1:", part1(rules, messages))
    print("Part 2:", part2(rules, messages))
