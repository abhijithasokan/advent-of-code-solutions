from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 14,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
import numpy as np
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    ch_to_ind = {'.' : 0, 'O': 1, '#': 2}
    return np.array([
        np.array([ch_to_ind[ch] for ch in row]) for row in inp_content
    ])
    

def solve_and_count(mat):
    ans = 0
    nn, mm = mat.shape

    for jj in range(mm):
        last_free_block = 0
        for ii in range(nn):
            if mat[ii][jj] == 1:
                last_free_block += 1
                ans += (nn - (last_free_block-1))
            elif mat[ii][jj] == 2:
                last_free_block = ii + 1

    return ans


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    mat = parse_input(input_str)
    return solve_and_count(mat)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat = parse_input(input_str) 

    def tilt(mat):
        nn, mm = mat.shape
        for jj in range(mm):
            last_free_block = -1
            for ii in range(nn):
                if mat[ii, jj] == 1:
                    last_free_block += 1
                    mat[ii, jj] = 0
                    mat[last_free_block, jj] = 1
                    
                elif mat[ii, jj] == 2:
                    last_free_block = ii 
        return mat
    
    def hash_key(mat):
        rows, cols = np.where(mat == 1)
        return tuple(rows), tuple(cols)

    cycle = 0
    
    mat_to_cycle = {}
    cycle_to_mat = {}

    TARGET_CYCLE = 1000000000
    while cycle <= TARGET_CYCLE:
        mat = tilt(mat) # tile north
        mat = tilt(mat.transpose()).transpose() # tilt west
        mat = tilt(mat[::-1])[::-1] # tilt south
        mat = np.rot90(tilt(np.rot90(mat, 1)), 3) # tilt east
        cycle += 1

        key = hash_key(mat)
        old_cycle = mat_to_cycle.get(key, None)
        if old_cycle is not None:
            period = cycle - old_cycle
            remaining = TARGET_CYCLE - cycle 
            equivalent_cycle = old_cycle + (remaining % period)

            # recreating the matrix (but all '.' chars will be '#')
            key2 = cycle_to_mat[equivalent_cycle]
            mat2 = np.ones_like(mat) * 2
            mat2[key2] = 1
            return solve_and_count(mat2)
        
        mat_to_cycle[key] = cycle
        cycle_to_mat[cycle] = key
        
    else:
        return solve_and_count(mat)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
