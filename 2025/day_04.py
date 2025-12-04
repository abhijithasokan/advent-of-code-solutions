from utils import aoc_comm, run_example
import os
import itertools

# --- update day/ year for each challenge
settings = {
    "day": 4,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    return [list(line) for line in inp_content]


def get_adj_pos(ii, jj, mat):
    nrows = len(mat)
    ncols = len(mat[0])
    for kk, ll in itertools.product([-1, 0, 1], repeat=2):
        if kk == 0 and ll == 0:
            continue
        ni, nj = ii + kk, jj + ll
        if 0 <= ni < nrows and 0 <= nj < ncols:
            yield ni, nj


def solve(mat, turn_off_cells=False):
    ans = 0
    for ii, jj in itertools.product(range(len(mat)), range(len(mat[0]))):
        if (
            mat[ii][jj] == "@"
            and sum(1 for ni, nj in get_adj_pos(ii, jj, mat) if mat[ni][nj] == "@") < 4
        ):
            ans += 1
            if turn_off_cells:
                mat[ii][jj] = "."
    return ans


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    mat = parse_input(input_str)
    return solve(mat, turn_off_cells=False)


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    mat = parse_input(input_str)
    ans = 0
    while True:
        cur_ans = solve(mat, turn_off_cells=True)
        ans += cur_ans
        if cur_ans == 0:
            break
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
