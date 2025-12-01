from math import dist
from regex import E
from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    "day": 1,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    for line in inp_content:
        direction = +1 if line[0] == "R" else -1
        yield direction, int(line[1:])


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)
    cur = 50
    ans = 0
    for direction, distance in inp:
        cur = (100 + cur + direction * (distance % 100)) % 100
        if cur == 0:
            ans += 1

    return ans


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)
    ans = 0
    cur_pos = 50
    for direction, distance in inp:
        rounds, rem = divmod(distance, 100)
        ans += rounds
        next_pos = cur_pos + direction * rem
        ans += 1 if (next_pos not in range(1, 100) and cur_pos != 0) else 0
        cur_pos = (100 + next_pos) % 100

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
