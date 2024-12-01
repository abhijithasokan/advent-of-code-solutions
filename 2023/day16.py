from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 16,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
import numpy as np
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    return inp_content
    



DIRECTION_MAP = {
    (-1, 0) : 'N',
    (1, 0) : 'S',
    (0, 1) : 'E',
    (0, -1) : 'W' 
}

DIRECTION_MAP2 = {v: k for k,v in DIRECTION_MAP.items()}
print(DIRECTION_MAP2)
REFLECTION_MAP = {
    '/' : {
        'N' : ['E'],
        'S' : ['W'],
        'E' : ['N'],
        'W' : ['S']
    }, 
    '\\' : {
        'N' : ['W'],
        'S' : ['E'],
        'E' : ['S'],
        'W' : ['N']
    },
    '|' : {
        'N' : ['N'],
        'S' : ['S'],
        'W' : ['N', 'S'],
        'E' : ['N', 'S']
    },
    '-' : {
        'N' : ['E', 'W'],
        'S' : ['E', 'W'],
        'E' : ['E'],
        'W' : ['W']
    },
    '.' : {
        'N' : ['N'],
        'S' : ['S'],
        'W' : ['W'],
        'E' : ['E']  
    }
}

def propagate_beam(mat, pos, last_pos, hits: set, visited_pos: set):
    stack = [(pos, last_pos)]
    visited = set()
    while stack:
        pos, last_pos = stack.pop()
        if (pos, last_pos) in visited:
            continue
        visited.add((pos, last_pos))
        direction = DIRECTION_MAP[(pos[0] - last_pos[0], pos[1] - last_pos[1])]
        visited_pos.add(pos)
        
        reflected_directions = REFLECTION_MAP[mat[pos[0]][pos[1]]][direction]
        dir_offsets = map(DIRECTION_MAP2.__getitem__, reflected_directions)
        for ff in dir_offsets:
            next_pos = (pos[0] + ff[0], pos[1] + ff[1])
            #print(pos, next_pos)
            if (next_pos[0] in range(0, len(mat))) and (next_pos[1] in range(0, len(mat[0]))):
                stack.append((next_pos, pos))

    






@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    mat = parse_input(input_str)
    visited = set()
    propagate_beam(mat, (0, 0), (0, -1), set(), visited)
    ans = len(visited)
    return ans
    


from collections import OrderedDict
@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat = parse_input(input_str)

    ans = 0

    for ii, off in [(0, -1), (len(mat)-1, 1)]:
        for jj in range(len(mat[0])):
            visited = set()
            propagate_beam(mat, (ii, jj), (ii + off, jj), set(), visited)
            ans = max(ans, len(visited))


    for jj, off in [(0, -1), (len(mat[0])-1, 1)]:
        for ii in range(len(mat)):
            visited = set()
            propagate_beam(mat, (ii, jj), (ii, jj + off ), set(), visited)
            ans = max(ans, len(visited))

    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
