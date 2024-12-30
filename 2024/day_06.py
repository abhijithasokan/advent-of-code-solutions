from utils import aoc_comm, run_example
import os


from collections import defaultdict

# --- update day/ year for each challenge
settings = {
    'day' : 6,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''
....#.....
.........#
..........
..#.......
.......#..
.........#
.#..^.....
........#.
#......#..
......#...
..#.......
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    grid = [list(line) for line in inp_content]
    start_pos = None
    for ii, line in enumerate(grid):
        if '^' in line:
            start_pos = (ii, line.index('^'))
            break    
    return grid, start_pos
    

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
CHANGE_DIR = lambda dd: (dd + 1) % len(DIRECTIONS)
TUPPLE_ADD = lambda x,y: (x[0]+y[0], x[1] + y[1])


def traverse(grid, pos):
    N, M = len(grid), len(grid[0])
    in_grid = lambda pos: (0 <= pos[0] < N) and (0 <= pos[1] < M)
    
    dd = 0
    while True:
        new_pos = TUPPLE_ADD(pos, DIRECTIONS[dd])
        if not in_grid(new_pos):
            grid[pos[0]][pos[1]] = '+'
            break

        if grid[new_pos[0]][new_pos[1]] == '#':
            dd = CHANGE_DIR(dd)
        else:
            grid[pos[0]][pos[1]] = '+'
            pos = new_pos
        
    return sum(line.count('+') for line in grid)


def traverse2(grid, pos):
    N, M = len(grid), len(grid[0])
    in_grid = lambda pos: (0 <= pos[0] < N) and (0 <= pos[1] < M)

    dd = 0
    poss = []

    def will_get_back(pos, dd):
        visited = set()
        while True:
            state = (pos, dd)
            if state in visited: # cycle in the offshoot path
                return True
            
            # cycle back to orig path
            if dd in visited_orig.get(state, []):
                return True
            
            visited.add(state)
            new_pos = TUPPLE_ADD(pos, DIRECTIONS[dd])

            if not in_grid(new_pos):
                return False
            
            if grid[new_pos[0]][new_pos[1]] == '#':
                dd = CHANGE_DIR(dd)
            else:
                pos = new_pos


    visited_orig = defaultdict(list)

    while True:
        visited_orig[pos].append(dd)

        new_pos = TUPPLE_ADD(pos, DIRECTIONS[dd])
        if not in_grid(new_pos):
            break    

        if grid[new_pos[0]][new_pos[1]] == '#':
            dd = CHANGE_DIR(dd)
        else:  
            if new_pos not in visited_orig:
                grid[new_pos[0]][new_pos[1]] = '#'
                if will_get_back(pos, CHANGE_DIR(dd)):
                    poss.append(new_pos)
                grid[new_pos[0]][new_pos[1]] = '.'

            pos = new_pos

    return len(set(poss))
        



@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    grid, start_pos = parse_input(input_str)
    return traverse(grid, start_pos)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    grid, start_pos = parse_input(input_str)
    return traverse2(grid, start_pos)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
