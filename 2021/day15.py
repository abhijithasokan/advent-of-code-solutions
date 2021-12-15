from utils import aoc_comm
import os
from collections import defaultdict
import itertools
import heapq

settings = {
    'day' : 15,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    mat = [list(map(int, ee)) for ee in inp_content.strip().split('\n')]
    return mat, len(mat), len(mat[0])


def get_surround_ind(ii, jj, r_sz, c_cz):
    shifts = itertools.product(range(-1, 2), range(-1, 2))
    coords = [(ii + x_shift, jj + y_shift) for x_shift, y_shift in shifts if (x_shift == 0 or y_shift == 0) and (x_shift != y_shift)]
    return filter(lambda coord: (coord[0] in range(r_sz) and coord[1] in range(c_cz)), coords)


def shortest_dist(adj_mat, end_node):
    pq = [(0, 0)]
    dists = [None]*(end_node+1)
    visited = set()

    while pq:
        dd, node = heapq.heappop(pq)
        if node == end_node:
            return dd
        if node in visited:
            continue
        visited.add(node)
        for adj_node, wt in adj_mat[node].items():
            if (dists[adj_node] is None) or (dists[adj_node] > dd + wt):
                dists[adj_node] = dd + wt
                heapq.heappush(pq, (dists[adj_node], adj_node))
    return


def build_matrix(mat, nn, mm, r_sz, c_sz):
    grid = [[0]*(c_sz*mm) for _ in range(r_sz*nn)]
    wrap_inc = lambda x: 1 if x == 9 else x + 1
    for ii in range(len(grid)):
        for jj in range(len(grid[0])):
            if ii in range(nn) and jj in range(mm):
                grid[ii][jj] = mat[ii][jj]
            else:
                up_ind, lef_ind = ii - nn, jj - mm
                up_val = grid[up_ind][jj] if up_ind >=0 else None
                lef_val = grid[ii][lef_ind] if lef_ind >= 0 else None
                if up_val is None or lef_val is None:
                    val = up_val or lef_val
                else:
                    val = max(up_val, lef_val)
                grid[ii][jj] = wrap_inc(val)
    return grid, len(grid), len(grid[0])


def solve(mat, nn, mm, grow_dim=None):
    if grow_dim is not None:
        mat, nn, mm = build_matrix(mat, nn, mm, *grow_dim)
    get_node_id = lambda x, y: x * nn + y
    adj_mat = defaultdict(dict)

    for ii, jj in itertools.product(range(nn), range(mm)):
        node1 = get_node_id(ii, jj)
        for xx, yy in get_surround_ind(ii, jj, nn, mm):
            node2 = get_node_id(xx, yy)
            adj_mat[node1][node2] = mat[xx][yy]

    return shortest_dist(adj_mat, nn * mm-1)


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    mat, nn, mm = parse_input(input_str)
    return solve(mat, nn, mm)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat, nn, mm = parse_input(input_str)
    return solve(mat, nn, mm, (5,5))


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
