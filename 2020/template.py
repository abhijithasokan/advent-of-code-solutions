from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 8,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip()
    # add further input processing here..
    yield None

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)

    ans = None
    for ee in inp:
        pass

    return ans # if 'ans' is None answer won't be submitted, else it will submit after confirmation 




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    ans = None
    for ee in inp:
        pass

    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    #l2_status = solve_l2()
    #print(l2_status)


if __name__ == '__main__':
    main()
