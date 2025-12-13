from functools import lru_cache
from platform import node
from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    "day": 11,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

EXAMPLE_INP_2 = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    adj_matrx = {}
    for line in inp_content:

        node, edges_str = line.split(":")
        adj_matrx[node] = edges_str.split()

    return adj_matrx


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    adj_matrix = parse_input(input_str)

    @lru_cache(maxsize=None)
    def dfs(node, end):
        if node == end:
            return 1
        res = 0
        for next_node in adj_matrix.get(node, []):
            res += dfs(next_node, end)
        return res

    return dfs("you", "out")


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    adj_matrix = parse_input(input_str)

    @lru_cache(maxsize=None)
    def dfs(node, end):
        if node == end:
            return 1
        res = 0
        for next_node in adj_matrix.get(node, []):
            res += dfs(next_node, end)
        return res

    ans = dfs("svr", "fft") * dfs("fft", "dac") * dfs("dac", "out")
    ans += dfs("svr", "dac") * dfs("dac", "fft") * dfs("dac", "out")
    return ans


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
