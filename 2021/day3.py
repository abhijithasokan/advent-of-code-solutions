from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 3,
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
        yield (ee)


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = list(parse_input(input_str))

    sz = len(inp)
    ln = len(inp[0])
    count_1bit = lambda ind: sum(1 for ii in range(sz) if inp[ii][ind] == '1')
    gamma_s = ''.join('1' if (count_1bit(ind) > sz / 2) else '0' for ind in range(ln))
    gamma = int(gamma_s, 2)
    alpha = (1<<len(gamma_s)) - 1 - gamma
    return gamma * alpha


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = list(parse_input(input_str))

    count_1bit = lambda ind: sum(1 for ii in range(len(inp)) if inp[ii][ind] == '1')
    mst_cmn_bit = lambda ind: '1' if (count_1bit(ind) >= len(inp)/2) else '0'

    def rating_filter():
        pos = 0
        nonlocal inp
        while len(inp) > 1:
            mc_bit = mst_cmn_bit(pos)
            #print(mc_bit)
            inp = list(filter(lambda ee: ee[pos] == mc_bit, inp))
            pos += 1
            #print(inp)
        return inp[0]


    inp_cp = inp.copy()
    ox_num = rating_filter()

    inp = inp_cp
    mst_cmn_bit = lambda ind: '0' if (count_1bit(ind) >= len(inp) / 2) else '1'

    co2_num = rating_filter()

    return int(ox_num, 2) * int(co2_num, 2)



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
