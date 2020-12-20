import re
from functools import reduce


def in_range(rule, field):
    for s, e in rule["range"]:
        if s <= field <= e:
            return True


def is_valid_field(rules, field):
    for rule in rules:
        if in_range(rule, field):
            return True
    return False


def part1(rules, ticket, nearby_tickets):
    res = 0
    for ticket in nearby_tickets:
        for field in ticket:
            if not is_valid_field(rules, field):
                res += field
    return res


def part2_dp(rules, ticket, nearby_tickets):
    """
    This is basically smart bruteforcing and assumes nothing about the data
    """
    fields_count = len(nearby_tickets[0])
    nearby_tickets = [
        nticket for nticket in nearby_tickets if not any(not is_valid_field(rules, field) for field in nticket)]

    # Save computation inside DP by caching the rules valid for each ticket field
    valid_rules = [list() for i in range(fields_count)]
    for index in range(fields_count):
        for i, rule in enumerate(rules):
            if all(in_range(rule, nticket[index]) for nticket in nearby_tickets):
                valid_rules[index].append(i)

    # Not the traditional way of implementing DP but makes more sense semantically
    dp = set()
    order = []

    def solve(bs):
        index = sum((bs >> i) & 1 for i in range(fields_count))

        if index >= fields_count:
            return True
        if bs in dp:
            return False

        for i in valid_rules[index]:
            used = ((bs >> i) & 1) == 1
            if used:
                continue
            order.append(i)
            if solve(bs | (1 << i)):
                return True
            order.pop()

        dp.add(bs)
        return False

    solve(0)

    return reduce(lambda a, x: a*(ticket[x[0]] if rules[x[1]]["name"].startswith("departure") else 1), enumerate(order), 1)


def part2_greedy(rules, ticket, nearby_tickets):
    """
    Since there's only one possible result we don't have to bruteforce every combination.
    There will be at least one field that has a single corresponding valid rule. We remove that rule 
    as a possibility from other fields.
    Now some other field will have one corresponding rule. Repeat the process until all fields have been assigned
    """
    nearby_tickets = [
        nticket for nticket in nearby_tickets if not any(not is_valid_field(rules, field) for field in nticket)]

    valid_rules = [list(range(len(rules))) for i in range(len(rules))]

    for nticket in nearby_tickets:
        for index, field in enumerate(nticket):
            next_valid_rules = list()
            for ir in valid_rules[index]:
                if in_range(rules[ir], field):
                    next_valid_rules.append(ir)
            valid_rules[index] = next_valid_rules

    used = [False for i in range(len(rules))]
    ans = 1

    for i, rules_list in sorted(enumerate(valid_rules), key=lambda x: len(x[1])):
        field_rule_idx = None
        for rule_idx in rules_list:
            if not used[rule_idx]:
                field_rule_idx = rule_idx
                break
        used[field_rule_idx] = True
        if rules[field_rule_idx]["name"].startswith("departure"):
            ans *= ticket[i]
    return ans


def process_input(file):
    raw_rules, raw_ticket, raw_nearby_tickets = file.read().split('\n\n')

    rules = [{"name": match.group(1), "range": [[int(num) for num in match.group(2).split('-')], [int(num) for num in match.group(3).split('-')]]}
             for match in [re.match(r'(.*): (\d+-\d+) or (\d+-\d+)', line) for line in raw_rules.splitlines()]]
    ticket = [int(field) for field in raw_ticket.splitlines()[1].split(',')]
    nearby_tickets = [[int(field) for field in raw_nticket.split(',')]
                      for raw_nticket in raw_nearby_tickets.splitlines()[1:]]

    return rules, ticket, nearby_tickets


if __name__ == "__main__":
    with open('../inputs/Day16.txt', 'r') as f:
        rules, ticket, nearby_tickets = process_input(f)
    print("Part 1:", part1(rules, ticket, nearby_tickets))
    # print("Part 2:", part2_dp(rules, ticket, nearby_tickets))
    print("Part 2:", part2_greedy(rules, ticket, nearby_tickets))
