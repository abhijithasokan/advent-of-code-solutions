from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 11,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    return inp_content 


def transpose(mat):
    return [ [mat[ii][ind] for ii in range(len(mat))] for ind in range(len(mat[0])) ]


def solve(mat, expand_num):
    row_inds = [ii for ii in range(len(mat)) if all(ch=='.' for ch in mat[ii])]
    mat = transpose(mat)
    col_inds = [ii for ii in range(len(mat)) if all(ch=='.' for ch in mat[ii])]
    mat = transpose(mat)

    n, m = len(mat), len(mat[0])

    def gen_ind_map(n, inds):
        ind_map = [0]*n
        ind = -1
        cur_exp = 0
        for ii in range(n):
            if cur_exp < len(inds) and (ii == inds[cur_exp]):
                ind += expand_num
                cur_exp += 1
            else:
                ind += 1
            ind_map[ii] = ind
        return ind_map

    row_mp = gen_ind_map(n, row_inds)
    col_mp = gen_ind_map(m, col_inds)

    pos = []
    for ii, line in enumerate(mat):
        for jj, ch in enumerate(line):
           if ch == '#':
               pos.append((row_mp[ii], col_mp[jj]))
    
    ans = 0
    for ii in range(len(pos)):
        for jj in range(ii, len(pos)):
            pos1, pos2 = pos[ii], pos[jj]
            moves = abs(pos1[0]- pos2[0]) + abs(pos2[1] - pos1[1])
            ans += moves
    
    return ans    


import numpy as np
@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    mat = parse_input(input_str)
    return solve(mat, 2)  


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat = parse_input(input_str)
    return solve(mat, 1000000)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
