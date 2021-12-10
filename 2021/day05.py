from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 5,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict


def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split('\n'):
        st, end = ee.split(' -> ')
        st = list(map(int, st.split(',')))
        end = list(map(int, end.split(',')))
        yield st, end

def get_coords(st, end, process_non_parallel_lines):
    if st[0] == end[0]:
        y1, y2 = st[1], end[1]
        y1, y2 = min(y1, y2), max(y1, y2)
        for y in range(y1, y2+1):
            yield st[0], y
    elif st[1] == end[1]:
        for x, y in get_coords(st[::-1], end[::-1], process_non_parallel_lines):
            yield y, x
    elif process_non_parallel_lines:
        if st[0] > end[0]:
            st, end = end, st

        inc = 1 if st[1] < end[1] else -1
        cur_y = st[1]
        for x in range(st[0], end[0] + 1):
            yield x, cur_y
            cur_y += inc

def count_overlap_points(inp, process_non_parallel_lines = False):
    grid = defaultdict(int)
    for st, end in inp:
        for coord in get_coords(st, end, process_non_parallel_lines):
            grid[coord] += 1
    count = sum(1 for val in grid.values() if val > 1)
    return count

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    return count_overlap_points(inp, False)




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    inp = parse_input(input_str)
    return count_overlap_points(inp, True)



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
