from utils import aoc_comm, run_example
import os

import re
import itertools


# --- update day/ year for each challenge
settings = {
    'day' : 14,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''


def parse_input(inp_content):
    for line in inp_content.strip().split('\n'):
        # print(line)
        yield tuple(map(int, re.match('p=(\d+),(\d+) v=([-]?\d+),([\-]?\d+)', line).groups()))


def move_bots(n, m, bot_data, time):
    grid = [[0]*m for _ in range(n)]
    for px, py, vx, vy in bot_data:
        jj, ii = px + vx*time, py + vy*time 
        ii %= n
        jj %= m
        grid[ii][jj] += 1
    return grid
    

@aoc_comm(settings, level = 1)
def solve_l1(input_str, dim): # input data will be passed to this as string 
    bot_data = list(parse_input(input_str))
    n, m = dim
    grid = move_bots(n, m, bot_data, time=100)

    safety_factor = 1
    for ii_region in [(0, n//2), (n//2 + 1, n)]:
        for jj_region in [(0, m//2), (m//2 + 1, m)]:
            count = 0
            for ii, jj in itertools.product(range(*ii_region), range(*jj_region)):
                count += grid[ii][jj]

            safety_factor *= count

    return safety_factor


def is_out_of_bound(pos, n, m):
    return not ( (0 <= pos[0] < n) and (0 <= pos[1] < m) )

def neighbours(pos, n, m, check_bound=True):
    ii, jj = pos
    for kk, ll in itertools.product(range(ii-1, ii+2), range(jj-1, jj+2)):
        if check_bound and is_out_of_bound((kk, ll), n, m):
            continue
        if ((kk, ll) != (ii, jj)):          
            yield (kk, ll)


@aoc_comm(settings, level = 2)
def solve_l2(input_str, dim): # input data will be passed to this as string 
    bot_data = list(parse_input(input_str))
    n, m = dim
    time = 1

    def check_sym(grid):
        visited = dict()
        def get_len(pos, cur_path):
            if (grid[pos[0]][pos[1]] == 0) or pos in cur_path:
                return None
            
            if pos in visited:
                return visited[pos]
            
            cur_path.add(pos)
            ln = 1
            for neig in neighbours(pos, n, m):
                nln = get_len(neig, cur_path)
                if nln is not None:
                    ln = max(ln, nln + 1)

            visited[pos] = ln
            return ln

        mx_ln = 0
        for pos in itertools.product(range(n), range(m)):
            nln = get_len(pos, set())
            if nln is not None:
                mx_ln = max(nln, mx_ln)

        return mx_ln > 20 # randomly decided threshold :)


    while True:
        grid = move_bots(n, m, bot_data, time=time)

        if check_sym(grid):
            for line in grid:
                print(''.join(' ' if ch == 0 else '+' for ch in line))
            
            print(time)

            if input() != '':
                os.system("clear")
                return time

        
        print(time)
        time += 1

    return None




def main():
    TEST_DIM = (7, 11)
    DIM = (103, 101)
    
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1, TEST_DIM))
    l1_status = solve_l1(DIM)
    print(l1_status)

    l2_status = solve_l2(DIM)
    print(l2_status)


if __name__ == '__main__':
    main()
