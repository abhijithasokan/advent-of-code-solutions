from utils import aoc_comm
import os

from collections import Counter

# --- update day/ year for each challenge
settings = {
    'day' : 1,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    l1, l2 = [], []
    for ee in inp_content:
        n1, n2 = ee.split()
        l1.append(int(n1))
        l2.append(int(n2))
    return l1, l2
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    l1, l2 = parse_input(input_str)
    l1.sort()
    l2.sort()
    ans = sum(abs(n1 - n2) for n1, n2 in zip(l1, l2))
    return ans




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    l1, l2 = parse_input(input_str)
    c1, c2 = Counter(l1), Counter(l2)
    ans = 0
    for loc_id, ct in c1.items():
        ans += loc_id * ct * c2[loc_id]
    return ans




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
