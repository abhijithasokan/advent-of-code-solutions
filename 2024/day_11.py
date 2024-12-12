from utils import aoc_comm, run_example
import os

from functools import lru_cache

# --- update day/ year for each challenge
settings = {
    'day' : 11,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''125 17
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    line = inp_content.strip()
    return list(map(int, line.split()))
    


def solve(nums, max_level):
    @lru_cache(maxsize=None)
    def count(num, level):
        if level == max_level:
            return 1
        
        if num == 0:
            return count(1, level + 1)
        
        snum = str(num)
        ns = len(snum)
        if len(snum) % 2 == 0:
            return count(int(snum[:ns//2]), level+1) + count(int(snum[ns//2:]), level+1)
        else:
            return count(num*2024, level + 1)

    return sum(count(num, 0) for num in nums)


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    nums = parse_input(input_str)
    return solve(nums, max_level=25)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    nums = parse_input(input_str)
    return solve(nums, max_level=75)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
