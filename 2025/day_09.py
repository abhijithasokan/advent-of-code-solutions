from curses.ascii import FS
from utils import aoc_comm, run_example
import os
import itertools

# --- update day/ year for each challenge
settings = {
    "day": 9,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip().split("\n")
    pos = [tuple(map(int, line.split(","))) for line in inp_content]
    return pos


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    pos = parse_input(input_str)
    ans = 0
    for p1, p2 in itertools.combinations(pos, 2):
        area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
        ans = max(ans, area)
    return ans


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    RG = lambda a, b: range(a, b + 1)

    def is_range_overlap(
        start1, end1, start2, end2
    ):  # overlap check, exclusing the single touch cases
        return start1 in RG(start2, end2 - 1) or end1 in RG(start2 + 1, end2)

    rot_coord = lambda x, y: (y, x)

    def is_line_overlapping_rect(ll, ur, p1, p2):
        if p1[0] == p2[0]:  # vertical line
            if p1[0] in RG(ll[0] + 1, ur[0] - 1):  # lies in x-range
                y1, y2 = sorted([p1[1], p2[1]])
                if is_range_overlap(ll[1], ur[1], y1, y2):
                    return True
            return False
        elif p1[1] == p2[1]:  # horizontal line
            return is_line_overlapping_rect(
                rot_coord(*ll), rot_coord(*ur), rot_coord(*p1), rot_coord(*p2)
            )
        raise ValueError("Found non-axis-aligned line")

    ans = 0
    pos = parse_input(input_str)
    for p1, p2 in itertools.combinations(pos, 2):
        ll = min(p1[0], p2[0]), min(p1[1], p2[1])
        ur = max(p1[0], p2[0]), max(p1[1], p2[1])

        filled = True
        for kk in range(len(pos)):
            pt1 = pos[kk]
            pt2 = pos[(kk + 1) % len(pos)]
            if is_line_overlapping_rect(ll, ur, pt1, pt2):
                filled = False
                break

        if filled:
            area = (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)
            ans = max(ans, area)

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
