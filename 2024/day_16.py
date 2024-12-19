from utils import aoc_comm, run_example
import os

import itertools
from collections import defaultdict
import heapq

# --- update day/ year for each challenge
settings = {
    'day' : 16,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def find_pos(grid, ch):
    return ((ii, jj) for ii, line in enumerate(grid) for jj, cc in enumerate(line) if cc == ch)

def parse_input(inp_content):
    inp_content = inp_content.strip()
    grid = inp_content.split('\n')
    
    start_pos = next(find_pos(grid, 'S'))
    end_pos = next(find_pos(grid, 'E'))
    return grid, start_pos, end_pos


SCOST, RCOST = 1, 1000
DIRECTION_TO_MOVEMENTS = {
    'N' : [((-1, 0), 'N', SCOST), ((0, 0), 'E', RCOST), ((0, 0), 'W', RCOST)],
    'S' : [((1, 0), 'S', SCOST), ((0, 0), 'E', RCOST), ((0, 0), 'W', RCOST)],
    'E' : [((0, 1), 'E', SCOST), ((0, 0), 'S', RCOST), ((0, 0), 'N', RCOST)],
    'W' : [((0, -1), 'W', SCOST), ((0, 0), 'S', RCOST), ((0, 0), 'N', RCOST)],
}


def get_neighbours(pos, di, n, m):
    for offset, ndi, cost in DIRECTION_TO_MOVEMENTS[di]:
        next_pos = (pos[0] + offset[0], pos[1] + offset[1])
        if (0 <= next_pos[0] < n) and (0 <= next_pos[1] < m):
            yield next_pos, cost, ndi



def build_adj_list(grid):
    adj_list = defaultdict(list)
    n, m = len(grid), len(grid[0])

    for ii, jj in itertools.product(range(n), range(m)):
        if grid[ii][jj] == '#':
            continue
        for dd in DIRECTION_TO_MOVEMENTS.keys():
            node = ((ii, jj), dd)
            for neig, cost, ndi in get_neighbours((ii, jj), dd, n, m):
                if grid[neig[0]][neig[1]] == '#':
                    continue
                neig_node = (neig, ndi)
                adj_list[node].append((neig_node, cost))

    return adj_list



def dijkstra_shortest_path(adj_list, start_node, end_nodes):
    distances = defaultdict(lambda : None)
    visited = set()

    heap = [(0, start_node)]

    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited:
            continue
        
        visited.add(node)
        distances[node] = dist

        if node in end_nodes:
            return distances, dist
        
        for nn, edge_w in adj_list[node]:
            if nn in visited:
                continue
            new_cost = dist + edge_w
            if (distances[nn] is None) or distances[nn] > new_cost:
                distances[nn] = new_cost
                heapq.heappush(heap, (distances[nn], nn))

    return None, None


def get_oppo_dir(di):
    TT = 'NSNEWE'
    return TT[TT.find(di)+1]


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    grid, start_pos, end_pos = parse_input(input_str)
    adj_list = build_adj_list(grid)
    targets = [(end_pos, di) for di in DIRECTION_TO_MOVEMENTS.keys()]
    _, dist = dijkstra_shortest_path(adj_list, (start_pos, 'E'), targets)
    return dist


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    grid, start_pos, end_pos = parse_input(input_str)
    adj_list = build_adj_list(grid)
    targets = [(end_pos, di) for di in DIRECTION_TO_MOVEMENTS.keys()]
    fwd_distances, min_cost = dijkstra_shortest_path(adj_list, (start_pos, 'E'), targets)
    
    # reverse distances
    targets2 = [(start_pos, get_oppo_dir('E'))] 
    all_bck_dists = {}
    for src in targets:
        dists_rev, min_cost2 = dijkstra_shortest_path(adj_list, src, targets2)
        if dists_rev is None or min_cost2 != min_cost:
            continue
        for node, dist in dists_rev.items():
            if node in all_bck_dists:
                all_bck_dists[node] = min(all_bck_dists[node], dist)
            else:
                all_bck_dists[node] = dist


    seats = set()
    for node, dist1 in fwd_distances.items():
        pos, di = node
        rev_node = (pos, get_oppo_dir(di))
        
        if rev_node not in all_bck_dists:
            continue

        if dist1 + all_bck_dists[rev_node] <= min_cost: # checks if it is possible to have a shortest path through this node
            seats.add(pos)
    
    return len(seats)




def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()











