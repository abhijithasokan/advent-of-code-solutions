from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 13,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n\n'))
    for block in inp_content:
        lines = block.strip().split()
        yield lines
    

import numpy as np
def solve(block, target_diff):
    def solve2(mat):
        n = len(mat)
        for ii in range(1, len(mat)):
            sz = min(ii, n-ii)
            diffs = (mat[ii-sz:ii] != mat[ii:ii+sz][::-1]).sum()
            if diffs == target_diff:
                return ii
            
        return None
            

    mat = np.array( [   np.array([1 if ch == '#' else 0 for ch in line]) for line in block   ])
    ans = solve2(mat)
    if ans is not None:
        return 100*ans 
    
    mat = mat.transpose()
    ans = solve2(mat)
    if ans is not None:
        return 1*ans 

    return None

@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str)
    ans = 0
    for block in inp:
        ans += solve(block, 0)

    return ans

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    ans = 0
    for block in inp:
        ans += solve(block, 1)

    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
