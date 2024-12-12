from utils import aoc_comm, run_example
import os

from functools import lru_cache
# --- update day/ year for each challenge
settings = {
    'day' : 10,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    return [list(map(int, line)) for line in inp_content]
    

def neighbours(pos, n, m):
    i, j = pos
    if i != 0:
        yield i-1, j
    if i != n - 1:
        yield i+1, j
    if j != 0:
        yield i, j-1
    if j != m - 1:
        yield i, j+1

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    mat = parse_input(input_str)
    n, m = len(mat), len(mat[0])

    def explore(pos, dests_reached):
        cur_level = mat[pos[0]][pos[1]]
        if cur_level == 9:
            dests_reached.add(pos)
            return 
        
        for ii, jj in neighbours(pos, n, m):
            pos2 = (ii, jj)
            if (mat[ii][jj] == cur_level + 1): 
                explore(pos2, dests_reached)

        return None

    ans = 0
    for ii, line in enumerate(mat):
        for jj, ele in enumerate(line):
            if ele == 0:
                dests_reached = set()
                explore((ii, jj), dests_reached) # no need to worry about cycles as the path only procceeds by climbing one level
                ans += len(dests_reached)

    return ans



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    mat = parse_input(input_str)
    n, m = len(mat), len(mat[0])

    def explore(pos):
        cur_level = mat[pos[0]][pos[1]]
        if cur_level == 9:
            return 1
        
        ans = 0
        for ii, jj in neighbours(pos, n, m):
            pos2 = (ii, jj)
            if (mat[ii][jj] == cur_level + 1):
                ans += explore(pos2)
        return ans

    ans = sum(explore((ii, jj)) for ii in range(n) for jj in range(m) if mat[ii][jj] == 0)
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
