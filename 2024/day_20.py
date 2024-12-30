from utils import aoc_comm, run_example
import os

from collections import defaultdict

# --- update day/ year for each challenge
settings = {
    'day' : 20,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1


def find_pos(grid, ch):
    return ((ii, jj) for ii, line in enumerate(grid) for jj, cc in enumerate(line) if cc == ch)

def parse_input(inp_content):
    inp_content = inp_content.strip()
    grid = inp_content.split('\n')
    
    start_pos = next(find_pos(grid, 'S'))
    end_pos = next(find_pos(grid, 'E'))
    grid = [list(line) for line in grid]
    return grid, start_pos, end_pos


def get_neighbours(pos, n, m):
    i, j = pos
    if i != 0:
        yield i-1, j
    if i != n - 1:
        yield i+1, j
    if j != 0:
        yield i, j-1
    if j != m - 1:
        yield i, j+1


PM_CHAR = '@'

def find_path(grid, start_pos, end_pos):
    n, m = len(grid), len(grid[0])
    cur_pos = start_pos
    path = []
    while cur_pos != end_pos:
        path.append(cur_pos)
        for ii, jj in get_neighbours(cur_pos, m, n):
            if grid[ii][jj] == '.' or grid[ii][jj] == 'E': 
                grid[ii][jj] = PM_CHAR
                cur_pos = (ii, jj)
                break

    if cur_pos != end_pos:
        raise ValueError("Path doesn't exist")
    
    path.append(end_pos)
    return path


def find_cheats(grid, pos, allowed_cost):
    n, m = len(grid), len(grid[0])
    targets_found = []
    for ii_off in range(-allowed_cost, allowed_cost+1):
        ii = pos[0] + ii_off
        if not ( 0 <= ii < n):
            continue

        jj_allowed_cost = allowed_cost - abs(ii_off)
        for jj_off in range(-jj_allowed_cost, jj_allowed_cost + 1):
            jj = pos[1] + jj_off
            if not ( 0 <= jj < m):
                continue

            if grid[ii][jj] == PM_CHAR:
                time_used = abs(ii_off) + abs(jj_off)
                targets_found.append(((ii, jj), time_used))

    return targets_found


def solve(parsed_inputs, allowed_cost):
    grid, start_pos, end_pos = parsed_inputs

    path = find_path(grid, start_pos, end_pos)
    pos_to_ind = { pos: ind for ind, pos in enumerate(path) }

    time_saved_to_cheat_count = defaultdict(int)

    for ind, pos in enumerate(path):
        for end_pos, time_used in find_cheats(grid, pos, allowed_cost):
            end_ind = pos_to_ind[end_pos]
            orig_time = end_ind - ind
            if orig_time < time_used:
                continue
            
            time_saved_to_cheat_count[orig_time - time_used] += 1
    
    ans = sum( count if time_saved >= 100 else 0 for time_saved, count in time_saved_to_cheat_count.items())
    return ans



@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    parsed_inputs = parse_input(input_str)
    return solve(parsed_inputs, allowed_cost=2)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    parsed_inputs = parse_input(input_str)
    return solve(parsed_inputs, allowed_cost=20)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
