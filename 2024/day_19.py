from utils import aoc_comm, run_example
import os

from functools import lru_cache


# --- update day/ year for each challenge
settings = {
    'day' : 19,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip()
    tows, pats = inp_content.split('\n\n')
    tows = tows.split(', ')
    pats = pats.split('\n')
    return tows, pats

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    tows, pats = parse_input(input_str)

    @lru_cache(maxsize=None)
    def solve(pat):
        if not pat:
            return True
        for tow in tows:
            if pat.startswith(tow) and solve(pat[len(tow):]):
                return True
        return False

    ans = sum(1 for pat in pats if solve(pat))
    return ans


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    tows, pats = parse_input(input_str)

    @lru_cache(maxsize=None)
    def solve(pat):
        if not pat:
            return 1
        nways = 0
        for tow in tows:
            if pat.startswith(tow):
                nways += solve(pat[len(tow):])
        return nways
    
    ans = sum(solve(pat) for pat in pats)
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
