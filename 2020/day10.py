from utils import aoc_comm
import os
import re
from collections import Counter, defaultdict

settings = {
    'day' : 10,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    for ee in inp_content:
        yield int(ee)

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = list(parse_input(input_str))

    inp = sorted(inp)
    device_adp = inp[-1] + 3
    inp.append(device_adp)
    cur = 0
    diffs = defaultdict(int)
    for ee in inp:
        if cur < ee <= cur + 3:
            diff = ee - cur
            cur = ee
            diffs[diff] += 1
        else:
            print("here")
    
    ans = diffs[1] * diffs[3]

    return ans 


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = list(parse_input(input_str))

    inp = sorted(inp)
    device_adp = inp[-1] + 3
    inp.append(device_adp)

    num_ways = defaultdict(int)

    num_ways[0] = 1
    for ind, ee in enumerate(inp):
        num_ways[ee] = num_ways[ee - 1] + num_ways[ee - 2] + num_ways[ee - 3]
        
    return (num_ways[device_adp])



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
