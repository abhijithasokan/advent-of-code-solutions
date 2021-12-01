from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 1,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split():
        yield int(ee)


def inc_count(inp):
    return sum(1 for ind in range(1, len(inp)) if inp[ind-1] < inp[ind] )

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = list(parse_input(input_str))
    return  inc_count(inp)




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = list(parse_input(input_str))
    new_inp = list( sum(inp[ind:ind+3]) for ind in range(len(inp)) )
    return inc_count(new_inp)



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
