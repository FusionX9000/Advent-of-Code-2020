from collections import deque
from functools import reduce


# Plenty of ways to solve this:
# * Infix to postfix then calculate with a stack,
# * Recursive function
# * CFG with some parser
# Here we only use a stack

def calculate(expression, precedence=None):
    operator = {'+': lambda a, b: a+b,
                '*': lambda a, b: a*b}

    if precedence == None:
        precedence = {'+': 1, '*': 1, '(': 0}

    i = 0
    stack = deque()

    while i < len(expression):
        char = expression[i]
        if char.isnumeric():
            num = int(char)
            while i+1 < len(expression) and expression[i+1].isnumeric():
                num = num*10 + int(expression[i])
                i += 1
            stack.append(num)
        elif char in operator:
            num = stack.pop()
            while len(stack) > 0 and precedence[stack[-1]] >= precedence[char]:
                num = operator[stack.pop()](stack.pop(), num)
            stack.append(num)
            stack.append(char)
        elif char == '(':
            stack.append('(')
        else:  # char == ')'
            num = stack.pop()
            while len(stack) > 0 and stack[-1] != '(':
                num = operator[stack.pop()](stack.pop(), num)
            stack.pop()
            stack.append(num)
        i += 1

    ans = stack.pop()
    while len(stack) > 0:
        ans = operator[stack.pop()](stack.pop(), ans)

    return ans


def part1(expressions):
    return reduce(lambda a, expression: a+calculate(expression), expressions, 0)


def part2(expressions):
    return reduce(lambda a, expression: a+calculate(expression, precedence={'+': 2, '*': 1, '(': 0}), expressions, 0)


def process_input(file):
    return [line.replace(' ', '') for line in file.read().splitlines()]


if __name__ == "__main__":
    with open('../inputs/Day18.txt', 'r') as f:
        expressions = process_input(f)
    print("Part 1:", part1(expressions))
    print("Part 2:", part2(expressions))
