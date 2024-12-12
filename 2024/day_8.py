from utils import aoc_comm, run_example
import os

from collections import defaultdict
import itertools

# --- update day/ year for each challenge
settings = {
    'day' : 8,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''2333133121414131402
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    
    char_to_inds = defaultdict(list)
    n, m = len(inp_content), len(inp_content[0])
    for ii, line in enumerate(inp_content):
        for jj, char in enumerate(line):
            if char.isalnum():
                char_to_inds[char].append((ii, jj))

    
    bound_check = lambda pos: (0 <= pos[0] < n) and (0 <= pos[1] < m)
    return char_to_inds, bound_check
    

TUP_ADD = lambda x, y: (x[0]+ y[0], x[1] + y[1])
TUP_NEG = lambda x: (-x[0], -x[1])

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    char_to_inds, bound_check = parse_input(input_str)
    antidodes_pos = set()

    for inds in char_to_inds.values():
        for pos1, pos2 in itertools.combinations(inds, 2):
            pos1, pos2 = min(pos1, pos2), max(pos1, pos2)
            diff = (pos2[0] - pos1[0], pos2[1] - pos1[1])

            a1 = TUP_ADD(pos1, diff)
            if a1 == pos2:
                a1 = TUP_ADD(pos1, TUP_NEG(diff))

            a2 = TUP_ADD(pos2, diff)
            if a2 == pos1:
                a2 = TUP_ADD(pos2, TUP_NEG(diff))

            if bound_check(a1):
                antidodes_pos.add(a1)
            if bound_check(a2):
                antidodes_pos.add(a2)

    ans =  len(antidodes_pos)
    return ans


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a%b)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    char_to_inds, bound_check = parse_input(input_str)
    antidodes_pos = set()
    for inds in char_to_inds.values():
        for pos1, pos2 in itertools.combinations(inds, 2):
            diff = (pos2[0] - pos1[0], pos2[1] - pos1[1])
            step = gcd(abs(diff[0]), abs(diff[1]))
            diff = ((diff[0])//step, (diff[1])//step)
            
            for dd in [diff, TUP_NEG(diff)]:
                a = pos1
                while bound_check(a):
                    antidodes_pos.add(a)
                    a = TUP_ADD(a, dd)

            antidodes_pos.add(pos1)
            antidodes_pos.add(pos2)
                
    ans =  len(antidodes_pos)
    return ans


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
