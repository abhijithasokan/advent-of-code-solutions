from utils import aoc_comm
import os
import re
import functools
import operator
import itertools

# --- update day/ year for each challenge
settings = {
    'day' : 3,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    return inp_content

    

def pick_num(mat, ii, jj):
    if not mat[ii][jj].isdigit():
        return None, None
    line = mat[ii]
    start_j, end_j = jj, jj+1
    while True:
        progress = False
        if start_j !=0 and line[start_j-1].isdigit():
            start_j -= 1
            progress = True
        if end_j != len(line) and line[end_j].isdigit():
            end_j += 1
            progress = True

        if not progress:
            break

    return int(line[start_j:end_j]), start_j
        

def surrounding_indices(mat, ii, jj):
    n, m = len(mat), len(mat[0])
    ii_s = [ii]
    if ii != 0:
        ii_s.append(ii-1)
    if ii != n-1:
        ii_s.append(ii+1)

    jj_s = [jj]
    if jj != 0:
        jj_s.append(jj-1)
    if jj != m-1:
        jj_s.append(jj+1)

    inidices = list(itertools.product(ii_s, jj_s))
    inidices.remove((ii, jj))
    return inidices
    

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    mat = parse_input(input_str)

    pos_to_nums = {}

    for ii, jj in itertools.product(range(len(mat)), range(len(mat[0]))):
        if not ( mat[ii][jj].isdigit() or mat[ii][jj] == '.' ):
            for ni, nj in surrounding_indices(mat, ii, jj):
                num, pos = pick_num(mat, ni, nj)
                if num is not None:
                    pos_to_nums[(ni, pos)] = num

    ans = sum(pos_to_nums.values())
    return ans
    




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat = parse_input(input_str)

    
    ans = 0
    for ii, jj in itertools.product(range(len(mat)), range(len(mat[0]))):
        if mat[ii][jj] == '*': 
            pos_to_nums = {}
            for ni, nj in surrounding_indices(mat, ii, jj):
                num, pos = pick_num(mat, ni, nj)
                if num is not None:
                    pos_to_nums[(ni, pos)] = num
                
            if len(pos_to_nums) == 2:
                v1, v2 = pos_to_nums.values()
                ans += v1*v2

    return ans




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
