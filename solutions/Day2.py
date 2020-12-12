import re
from collections import namedtuple

def part1(pass_policies):
    def isValid(password, policy):
        count = 0
        for char in password:
            if char==policy.char:
                count+=1
                if(count>policy.maxCount):
                    return False
        return count>=policy.minCount

    ans=0
    Policy = namedtuple('Policy', ['minCount', 'maxCount', 'char'])
    
    for password, policy_tuple in pass_policies:
        minCount, maxCount, char = policy_tuple
        policy = Policy(minCount, maxCount, char)
        if isValid(password, policy):
            ans+=1
    return ans

def part2(pass_policies):
    def isValid(password, policy):
        return (password[pos1-1]==policy.char)^(password[pos2-1]==policy.char)

    ans=0
    Policy = namedtuple('Policy', ['pos1', 'pos2', 'char'])

    for password, policy_tuple in pass_policies:
        pos1, pos2, char = policy_tuple
        policy = Policy(pos1, pos2, char)
        if isValid(password, policy):
            ans+=1
    return ans

def process_input(input_):
    pattern = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)')

    parsed_lines = (re.match(pattern, line).groups() for line in input_)
    pass_policies = [(password, (int(num1),int(num2),char)) for num1, num2, char, password in parsed_lines]

    return pass_policies

if __name__ == "__main__":
    with open('../inputs/Day2.txt','r') as f:
        pass_policies = process_input(f.readlines())

    print("Part 1:", part1(pass_policies))
    print("Part2 2:", part2(pass_policies))
    