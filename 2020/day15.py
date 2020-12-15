from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 15,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip().split(',')
    for ee in inp_content:
        yield int(ee)


def get_nth_num_in_game(nn, numbers):
    last_seen = {}
    last = numbers[0]
    for time, ee in enumerate(numbers[1:]):
        last_seen[last] = time
        last = ee
        
    for time in range(len(numbers), nn):
        if last in last_seen:
            cur = time - last_seen[last] - 1
        else:
            cur = 0
        last_seen[last] = time - 1
        last = cur

    return cur


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = list(parse_input(input_str))
    ans = get_nth_num_in_game(2020, inp)
    return ans 



@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = list(parse_input(input_str))
    ans = get_nth_num_in_game(30000000, inp)
    return ans 



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
