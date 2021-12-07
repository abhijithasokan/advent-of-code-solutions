from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 7,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools
from statistics import mean


def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split(','):
        yield int(ee)



@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    # Complexity - 0(max(inp) - min(inp)) + 0(N.log(N))
    inp = list(parse_input(input_str))
    inp.sort()
    crab_ind = 0
    bk_sum, fw_sum = 0, sum(inp)
    min_cost = sum(inp) - inp[0] * len(inp)
    for x_cord in range(inp[0], inp[-1]+1):
        if x_cord > inp[crab_ind]:
            crab_ind += 1

        if x_cord == inp[crab_ind]:
            new_ind = crab_ind
            while (new_ind + 1) < len(inp) and inp[new_ind+1] == inp[new_ind]:
                new_ind += 1

            same_pos_count = new_ind - crab_ind + 1
            fw_sum -= same_pos_count*inp[new_ind]
            cost = fw_sum - inp[crab_ind] * (len(inp) - new_ind-1) + inp[crab_ind] * (crab_ind) -  bk_sum
            bk_sum += same_pos_count*inp[new_ind]
            crab_ind = new_ind
        else:
            cost = fw_sum - x_cord * (len(inp) - crab_ind-1) + x_cord * crab_ind -  bk_sum

        min_cost = min(cost, min_cost)

    return min_cost




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = list(parse_input(input_str))
    ff = lambda x: x*(x+1)//2
    min_cost = min(sum(ff(abs(pos - coord)) for pos in inp) for coord in range(min(inp), max(inp)+1))
    return min_cost



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
