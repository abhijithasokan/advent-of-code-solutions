from utils import aoc_comm, run_example
import os

import itertools
from collections import defaultdict
import heapq
import sys

# --- update day/ year for each challenge
settings = {
    'day' : 18,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''
'''

EXAMPLE_INP_2 = '''
'''

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    positions = [(int(a), int(b)) for a, b in (line.split(',') for line in inp_content)]
    n = max(max(p[0] for p in positions), max(p[1] for p in positions)) + 1
    return n, positions


def dijkstra_shortest_path(adj_list, start_node, end_node):
    distances = defaultdict(lambda : None)
    visited = set()

    heap = [(0, start_node)]

    while heap:
        dist, node = heapq.heappop(heap)
        if node in visited:
            continue

        if node == end_node:
            return dist
        
        visited.add(node)
        distances[node] = dist

        for nn, edge_w in adj_list[node]:
            if nn in visited:
                continue
            new_cost = dist + edge_w
            if (distances[nn] is None) or distances[nn] > new_cost:
                distances[nn] = new_cost
                heapq.heappush(heap, (distances[nn], nn))

    return None

    
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


def build_adj_list_for_grid(n, positions):
    adj_list = defaultdict(list)
    positions = set(positions)
    for node in itertools.product(range(n), range(n)):
        if node in positions:
            continue
        for neig in get_neighbours(node, n, n):
            if neig in positions:
                continue
            adj_list[node].append( (neig, 1) )
    return adj_list


INDEX = 1024

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    n, positions = parse_input(input_str)
    adj_list = build_adj_list_for_grid(n, positions[:INDEX+1])
    return dijkstra_shortest_path(adj_list, (0, 0), (n-1, n-1))


def remove_node(adj_list, node, n):
    if node in adj_list:
        for neig in get_neighbours(node, n, n):
            if node in adj_list[neig]: 
                adj_list[neig].remove(node)
        
        del adj_list[node]

@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    n, positions = parse_input(input_str)
    index = INDEX 

    adj_list = build_adj_list_for_grid(n, positions[:INDEX+1])
    
    # NOTE: Here I'm doing a linear search to find the node
    # A more optimal solution would be to do **Binary search** instead
    while index < len(positions):
        remove_node(adj_list, positions[index], n)
        ans = dijkstra_shortest_path(adj_list, (0, 0), (n-1, n-1))
    
        if ans is None:
            x, y = positions[index]
            return f'{x},{y}'
        
        index += 1

    return None



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
