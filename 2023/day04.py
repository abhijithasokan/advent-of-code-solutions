from utils import aoc_comm
import os
import re
import functools
import operator
import itertools

# --- update day/ year for each challenge
settings = {
    'day' : 4,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    for line in inp_content:
        win_nums, nums = line[line.find(':')+1:].strip().split('|')
        yield list(map(int, win_nums.split())), list(map(int, nums.split()))

    





@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)

    ans = 0
    for win_nums, nums in inp:
        overlap_count = len(set(win_nums) & set(nums))
        if overlap_count:
            ans += 2**(overlap_count-1)

    return ans




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = list(parse_input(input_str))

    card_count = [1]*len(inp)
    for ind, (win_nums, nums) in enumerate(inp):
        overlap_count = len(set(win_nums) & set(nums)) 
        if overlap_count:
            for ii in range(ind+1, ind+overlap_count+1):
                card_count[ii] += card_count[ind]

    return sum(card_count)




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
