from numpy import sort
from utils import aoc_comm, run_example
import os
from collections import deque

# --- update day/ year for each challenge
settings = {
    "day": 7,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    return [list(line) for line in inp_content]


def traverse(matrix):
    nn, mm = len(matrix), len(matrix[0])
    start_pos = 1, matrix[0].index("S")

    dq = deque()
    dq.append(start_pos)

    split_loc = set()
    while dq:
        pos = dq.popleft()
        ii, jj = pos[0], pos[1]
        if ii >= nn:
            continue
        if matrix[ii][jj] == "^":
            split_loc.add((ii, jj))
            if jj - 1 >= 0 and matrix[ii][jj - 1] != "|":
                matrix[ii][jj - 1] = "|"
                dq.append((ii + 1, jj - 1))
            if jj + 1 < mm and matrix[ii][jj + 1] != "|":
                matrix[ii][jj + 1] = "|"
                dq.append((ii + 1, jj + 1))
        else:
            matrix[ii][jj] = "|"
            dq.append((ii + 1, jj))

    return split_loc


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    matrix = parse_input(input_str)
    split_locs = traverse(matrix)
    return len(split_locs)


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    matrix = parse_input(input_str)
    nn = len(matrix)
    start_pos = 1, matrix[0].index("S")

    _ = traverse(matrix)

    memo_table = {}

    def dp(ii, jj):
        if ii == nn:
            return 1

        if matrix[ii][jj] == "|":
            return dp(ii + 1, jj)

        if matrix[ii][jj] == "^":
            cache_res = memo_table.get((ii, jj), None)
            if cache_res is not None:
                return cache_res

            res = dp(ii + 1, jj - 1) + dp(ii + 1, jj + 1)
            memo_table[(ii, jj)] = res
            return res

        raise RuntimeError("Not an expected case")

    return dp(*start_pos)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
