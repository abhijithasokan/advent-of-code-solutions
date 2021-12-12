from utils import aoc_comm
import os
from collections import defaultdict

settings = {
    'day' : 12,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    adj_list = defaultdict(list)
    for ee in inp_content.split():
        v1, v2 = ee.split('-')
        adj_list[v1].append(v2)
        adj_list[v2].append(v1)
    return adj_list


def dfs2(node: str, adj_list: defaultdict, visited: set):
    if not hasattr(dfs2, 'double_node'):
        dfs2.double_node = None

    if node == 'end':
        return 1
    if node == 'start' and node in visited:
        return 0

    if node.islower():
        if node not in visited:
            visited.add(node)
        elif dfs2.double_node is None:
            dfs2.double_node = node
        else:
            return 0

    paths_here = 0
    for v2 in adj_list[node]:
        paths_here += dfs2(v2, adj_list, visited)

    if node.islower():
        if node == dfs2.double_node:
            dfs2.double_node = None
        else:
            visited.discard(node)
    return paths_here


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    adj_list = parse_input(input_str)
    dfs2.double_node = not None
    ans = dfs2('start', adj_list, set())
    dfs2.double_node = None
    return ans


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    adj_list = parse_input(input_str)
    dfs2.double_node = None
    ans = dfs2('start', adj_list, set())
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
