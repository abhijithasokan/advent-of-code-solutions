from utils import aoc_comm
import os

# --- update day/ year for each challenge
settings = {
    'day' : 8,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

import re
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n\n'))
    directions = inp_content[0]

    paths = re.findall('(\w+) = \((\w+), (\w+)\)', inp_content[1])
    return directions, paths


def walk(directions, paths, cur = 'AAA', stop_at_z_ending=False):
    step_num = 0
    while True:
        dd = directions[step_num % len(directions)]
        dd = 0 if dd == 'L' else 1
        cur = paths[cur][dd]
        if cur == 'ZZZ' or (stop_at_z_ending and cur.endswith('Z')):
            break
        step_num += 1

    return step_num + 1


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    directions, paths = parse_input(input_str)
    path_map = {ss: (ll, rr) for ss, ll, rr in paths}
    ans = walk(directions, path_map)
    return ans


import functools
def lcm_list(nums):
    def gcd(a, b):
        if b==0:
            return a
        return gcd(b, a%b)

    lcm = lambda a, b: a*b // gcd(a, b)
    return functools.reduce(lcm, nums, 1)


from collections import defaultdict
def multi_walk(directions, paths):
    heads = list(filter(lambda x: x.endswith('A'), paths.keys()))
    return lcm_list(walk(directions, paths, hh, stop_at_z_ending=True) for hh in heads)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    directions, paths = parse_input(input_str)
    path_map = {ss: (ll, rr) for ss, ll, rr in paths}
    return multi_walk(directions, path_map)
    

def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
