from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 14,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    ini = []
    for ee in inp_content:
        if ee.startswith("mask"):
            mask = (ee.split(' = ')[1].strip())
            ini.append((-1, mask))
        else:
            add, val = ee.replace("mem[","").replace("] = ", ",").split(",")
            ini.append( (int(add.strip()), int(val.strip()) ) )
        
    return ini

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    ini = parse_input(input_str)

    arr_sz = max( ee[0] for ee in ini)
    arr = [0]*arr_sz

    cur_mask = 'X'*36
    for ind, val in ini:
        if ind == -1:
            cur_mask = val
            mask1 = int(cur_mask.replace('1','0').replace('X','1'), 2)
            mask2 = int(cur_mask.replace('X','0'), 2)
        else:
            arr[ind-1] = (val&mask1) | mask2

    ans = sum(arr)
    return ans 




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    ini = parse_input(input_str)
    arr = defaultdict(int)

    cur_mask = 'X'*36
    for ind2, val in ini:
        if ind2 == -1:
            cur_mask = val
            mask1 = int(cur_mask.replace('1','0').replace('X','1'), 2)
            mask2 = int(cur_mask.replace('X','0'), 2)
            mask3 = int(cur_mask.replace('0','1').replace('X','0'), 2)
        else:
            poss = [ ind  if ch == 'X' else None for ind, ch in enumerate(cur_mask)  ]
            poss = list(filter(lambda x: x is not None, poss))
            for ii in range(0, len(poss) + 1):
                for cm in itertools.chain([()], itertools.combinations(poss, ii)):
                    new_mask = list(cur_mask)
                    for ee1 in cm:
                        new_mask[ee1] = '1'
    
                    new_mask = ''.join(new_mask)
                    new_mask = int(new_mask.replace('X','0'), 2)
                    addrr =  ( (mask2 | ind2) & mask3) | new_mask
                    arr[addrr] = val

    ans = sum(arr.values())
    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
