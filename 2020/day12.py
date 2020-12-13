from utils import aoc_comm
import os
import re
from collections import Counter, defaultdict


settings = {
    'day' : 12,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}



def parse_input(inp_content):
    inp_content = inp_content.strip().split()
    for ee in inp_content:
        yield ee[0], int(ee[1:])
    

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    inp = parse_input(input_str)

    cur_dir = 'E'
    directions = 'NWSE'
    dist = { x:0 for x in directions }
    dmap = { ee:ind  for ind, ee in enumerate(directions) }
    for dd, val in inp:
        if dd == 'F':
            dist[cur_dir] += val
        elif dd in directions:
            dist[dd] += val
        elif dd == 'L':
            turn = (val//90)%4
            cur_dir = directions[(directions.index(cur_dir) + turn)%4]
        elif dd == 'R':
            turn = (val//90)%4
            cur_dir = directions[(4+ directions.index(cur_dir) - turn)%4]
        
    ans = abs(dist['N'] - dist['S']) + abs(dist['E'] - dist['W'])
    return ans 




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    cur_dir = 'E'
    directions = 'NWSE'
    dist = { x:0 for x in directions }
    wp = { x:0 for x in directions }
    dmap = { ee:ind  for ind, ee in enumerate(directions) }

    wp['N'] = 1
    wp['E'] = 10
    
    for dd, val in inp:
        if dd == 'F':
            for aa, bb in wp.items():
                dist[aa] += bb*val
        elif dd in directions:
            wp[dd] += val
        elif dd == 'L':
            turn = (val//90)%4
            nwp = {}
            for aa,bb in wp.items():
                nwp[directions[(directions.index(aa) + turn)%4]] = bb
            wp = nwp
        elif dd == 'R':
            turn = (val//90)%4
            nwp = {}
            for aa,bb in wp.items():
                nwp[directions[(directions.index(aa) - turn)%4]] = bb
            wp = nwp

    ans = abs(dist['N'] - dist['S']) + abs(dist['E'] - dist['W'])
    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
