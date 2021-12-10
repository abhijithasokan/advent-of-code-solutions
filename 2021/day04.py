from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 4,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict



def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n\n')
    called_out = list(map(int, inp_content[0].split(',')))
    grids = []
    for mt_s in inp_content[1:]:
        rows = mt_s.split('\n')
        grid = [ list(map(int, r.split())) for r in rows]
        grids.append(grid)
    return called_out, grids

def solve(called_out, grids, find_last = False):
    mat_to_turn = {}
    for ind, grid in enumerate(grids):
        r_sz, c_sz = len(grid[0]), len(grid)
        ele_to_coord = {}
        sm = 0
        for rn, row in enumerate(grid):
            for cn, col in enumerate(row):
                ele_to_coord[col] = (rn, cn)
                sm += col

        filled_r = defaultdict(int)
        filled_c = defaultdict(int)

        marked_out_sm = 0
        for turn, item in enumerate(called_out):
            coord = ele_to_coord.get(item, None)
            if coord is None:
                continue
            rn, cn = coord
            marked_out_sm += item
            filled_r[rn] += 1
            filled_c[cn] += 1
            if filled_r[rn] == r_sz or filled_c[cn] == c_sz:
                mat_to_turn[ind] = (turn, item * (sm - marked_out_sm))
                break

    criteria = max if find_last else min
    score = criteria(mat_to_turn.values(), key=lambda xx: xx[0])[1]
    return score


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    called_out, grids = parse_input(input_str)
    return solve(called_out, grids)



@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    called_out, grids = parse_input(input_str)
    return solve(called_out, grids, find_last=True)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
