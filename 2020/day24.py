from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 24,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    # add further input processing here..
    return inp_content

DIRECTIONS = ['e', 'se', 'sw', 'w', 'nw', 'ne']
def get_drections(ss):
    cur = ''
    path = []
    for ee in ss:
        cur = cur + ee
        if cur in DIRECTIONS:
            path.append(cur)
            cur = ''
    return path

OFFSET_MAPPING = {
    'e'  : (1, 0),
    'w'  : (-1, 0),
    'se' : (0, -1),
    'sw' : (-1, -1),
    'nw' : (0, 1),
    'ne' : (1, 1)
}

def get_next_pos(step, pos):
    x_offset, y_offset = OFFSET_MAPPING[step]
    return pos[0] + x_offset, pos[1] + y_offset
    

def get_pos(dirs, pos):
    for step in dirs:
        pos = get_next_pos(step, pos)
    return pos

def get_neighbours(pos):
    poss = []
    for step in DIRECTIONS:
        poss.append(get_next_pos(step, pos))
    return poss
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str)

    ans = None
    flipped = set()
    for ee in inp:
        dirs = get_drections(ee)
        pos = get_pos(dirs, (0,0))
        if pos in flipped:
            flipped.discard(pos)
        else:
            flipped.add(pos)

    ans = len(flipped)
    return ans

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    ans = None
    black_tiles = set()
    for ee in inp:
        dirs = get_drections(ee)
        pos = get_pos(dirs, (0,0))
        if pos in black_tiles:
            black_tiles.discard(pos)
        else:
            black_tiles.add(pos)

    for day in range(1, 101):
        next_black_tiles = set()
        neighbours = set()
        
        new_neig = set()
        for pos1 in black_tiles:
            neig = get_neighbours(pos1)
            neighbours.update( neig )
            ct = sum( 1 if nn in black_tiles else 0 for nn in neig )
            if not (ct == 0 or ct >  2):
                next_black_tiles.add(pos1)

        white_neigh = neighbours - black_tiles
                
        for pos in white_neigh:
            neig = get_neighbours(pos)
            ct = sum( 1 if nn in black_tiles else 0 for nn in neig )
            if ct == 2:
                next_black_tiles.add(pos)

        black_tiles = next_black_tiles
            
    ans = len(black_tiles)        
    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
