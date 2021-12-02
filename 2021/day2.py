from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 2,
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
    for ee in inp_content.split('\n'):
        xx = ee.split(' ')
        yield xx[0], int(xx[1])

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    hor = 0
    depth = 0
    for dir, val in inp:
        if dir == 'forward':
            hor += val
        elif dir == 'down':
            depth += val
        elif dir == 'up':
            depth -= val
    return hor * depth


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    hor = 0
    depth = 0
    aim = 0
    for dir, val in inp:
        if dir == 'forward':
            hor += val
            depth += aim * val
        elif dir == 'down':
            aim += val
        elif dir == 'up':
            aim -= val
    return hor * depth



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
