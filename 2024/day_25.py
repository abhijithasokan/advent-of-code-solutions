from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    'day' : 25,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

from collections import Counter
# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
'''

EXAMPLE_INP_2 = '''
'''

def parse_input(inp_content):
    grids = inp_content.strip().split('\n\n')
    keys = []
    locs = []
    for grid in grids:
        grid = grid.split('\n')
        n, m = len(grid), len(grid[0])
        trans = [ ''.join(grid[ii][jj] for ii in range(n)) for jj in range(m) ]

        heights = tuple(line.count('#') for line in trans)
        if grid[0].count('#') == m:
            keys.append(heights)
        else:
            locs.append(heights)
    
    return locs, keys

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    locs, keys = parse_input(input_str)

    ans = 0
    for key in keys:
        mt = tuple(7-h for h in key)
        for loc in locs:
            if all(lh >= mh for lh, mh in zip(mt, loc)):
                ans += 1 
    
    return ans


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

if __name__ == '__main__':
    main()
