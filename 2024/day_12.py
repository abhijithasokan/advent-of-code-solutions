from utils import aoc_comm, run_example
import os

import itertools
from collections import defaultdict
from dataclasses import dataclass, field


# --- update day/ year for each challenge
settings = {
    'day' : 12,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    return [list(line) for line in inp_content]
    
def is_out_of_bound(pos, n, m):
    return not ( (0 <= pos[0] < n) and (0 <= pos[1] < m) )

def neighbours(pos, n, m, check_bound=True):
    ii, jj = pos
    for kk, ll in itertools.product(range(ii-1, ii+2), range(jj-1, jj+2)):
        if check_bound and is_out_of_bound((kk, ll), n, m):
            continue
        if ((kk, ll) != (ii, jj)):          
            yield (kk, ll)
    



@dataclass
class RegionData:
    crop: str = ''
    perimeter: int = 0
    area: int = 0
    cur_set: set = field(default_factory=set)
    vert_lines : dict = field(default_factory = lambda: defaultdict(lambda : ([], [])))
    hori_lines : dict = field(default_factory = lambda: defaultdict(lambda : ([], [])))

    def compute_num_sides(self):
        num_sides = 0
        for lines in itertools.chain(self.vert_lines.values(), self.hori_lines.values()):
            for line in lines:
                line.sort()
                nsides = sum( 1 for p1, p2 in zip(line[:-1], line[1:]) if (p1+1)!=p2)
                nsides += (1 if len(line) else 0)
                num_sides += nsides
        return num_sides




def explore(pos, region_data, mat, line_tracking=False):
    if pos in region_data.cur_set:
        return
    
    n, m = len(mat), len(mat[0])
    region_data.cur_set.add(pos)
    region_data.area += 1

    for (ii, jj) in neighbours(pos, n, m, check_bound=False):
        if ii == pos[0] or jj == pos[1]: # up/left/right/down only
            if (not is_out_of_bound((ii, jj), n, m)) and (mat[ii][jj] == region_data.crop):
                explore((ii, jj), region_data, mat, line_tracking)
            else:
                region_data.perimeter += 1
                if line_tracking:
                    if ii == pos[0]:
                        region_data.vert_lines[jj][int(jj==pos[1]-1)].append(ii)
                    if jj == pos[1]:
                        region_data.hori_lines[ii][int(ii==pos[0]-1)].append(jj)
    return None




def solve(mat, level):
    n, m = len(mat), len(mat[0])
    line_tracking = True if level == 2 else False
    visited = set()
    ans = 0

    for ii, jj in itertools.product(range(n), range(m)):
        if (ii, jj) in visited:
            continue

        region_data = RegionData(mat[ii][jj])
        explore((ii, jj), region_data, mat, line_tracking)
        if level == 1:
            ans += region_data.area * region_data.perimeter
        else:
            ans += region_data.area * region_data.compute_num_sides()
        visited |= region_data.cur_set

    return ans



@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    mat = parse_input(input_str)
    return solve(mat, level=1)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    mat = parse_input(input_str)
    return solve(mat, level=2)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
