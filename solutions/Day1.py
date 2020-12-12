def part1(nums):
    l,r = 0, len(nums)-1
    while l<r:
        if nums[l]+nums[r]<2020:
            l+=1
        elif nums[l]+nums[r]>2020:
            r-=1
        else:
            return nums[l]*nums[r]
    return -1


def part2(nums):
    for i in range(0, len(nums)):
        l,r = 0, len(nums)-1
        while(l<i and i<r):
            three_sum = sum((nums[i],nums[l],nums[r]))
            if(three_sum>2020):
                r-=1
            elif three_sum<2020:
                l+=1
            else:
                return nums[i]*nums[l]*nums[r]
    return -1
    
def process_input(input_):
    return sorted([int(num) for num in input_])

if __name__ == "__main__":
    with open('../inputs/Day1.txt','r') as f:
        nums = process_input([line.rstrip() for line in f])
    print("Part 1: ", part1(nums))
    print("Part 2: ", part2(nums))
