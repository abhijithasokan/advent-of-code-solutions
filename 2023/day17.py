from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 17,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
import numpy as np
def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    arr = np.array([
        np.array(list(map(int, line))) for line in inp_content
    ])
    return arr
    

import itertools
def get_adjacent_nodes(mat, pos, level, jumps_allowed):
    ii, jj = pos
    for offset in jumps_allowed:
        neighbour = (ii + level * offset, jj + (1 - level)*offset)
        if (neighbour[0] in range(0, len(mat))) and (neighbour[1] in range(0, len(mat[0]))):
            yield neighbour


def edge_weight(mat, pos1, pos2):
    i1, j1 = pos1
    i2, j2 = pos2
    if i1 > i2:
        i1, i2 = i2, i1
    if j1 > j2:
        j1, j2 = j2, j1

    sm = int(mat[i1:i2+1, j1:j2+1].sum())
    return sm - mat[pos1[0], pos1[1]]


import heapq
from collections import defaultdict

def shortest_path(start_pos, end_pos, mat, jumps_allowed):
    LIM_DIST = mat.sum() * 100

    dist_visited = defaultdict(int)
    dist_unvisited = defaultdict(lambda : LIM_DIST)
    
    to_visit = []
    heapq.heappush(to_visit, (0, (start_pos, 1)))
    dist_unvisited[(start_pos, 1)] = 0

    heapq.heappush(to_visit, (0, (start_pos, 0)))
    dist_unvisited[(start_pos, 0)] = 0

    prev = {(start_pos, 0): None, (start_pos, 1): None}

    while to_visit:
        dist, node = heapq.heappop(to_visit)
        if node in dist_visited:
            continue

        pos, level = node
        
        dist_visited[node] = dist
        for neighbour in get_adjacent_nodes(mat, pos, level, jumps_allowed):
            neighbour_node = (neighbour, 1-level)
            if neighbour_node not in dist_visited:
                new_dist = dist + edge_weight(mat, pos, neighbour)
                if new_dist < dist_unvisited[neighbour_node]:
                    dist_unvisited[neighbour_node] = new_dist
                    heapq.heappush(to_visit, (new_dist, neighbour_node))
                    prev[neighbour_node] = node


    return min(dist_visited[(end_pos, 1)], dist_visited[(end_pos, 0)])




@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    mat = parse_input(input_str)
    jumps_allowed = list(itertools.chain(range(-3, 0), range(1, 4)))
    ans = shortest_path((0, 0), (len(mat)-1, len(mat[0])-1), mat, jumps_allowed)
    return ans
    

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat = parse_input(input_str)
    jumps_allowed = list(itertools.chain(range(-10, -3), range(4, 11)))
    ans = shortest_path((0, 0), (len(mat)-1, len(mat[0])-1), mat, jumps_allowed)
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
