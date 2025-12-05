from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    "day": 5,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n\n")
    id_ranges = []
    for line in inp_content[0].split("\n"):
        a, b = sorted(map(int, line.split("-")))
        id_ranges.append((a, b))

    ids = list(map(int, inp_content[1].split("\n")))
    return id_ranges, ids


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    id_ranges, ids = parse_input(input_str)
    id_ranges = [range(a, b + 1) for a, b in id_ranges]
    ans = 0
    for id_ in ids:
        if any(id_ in r for r in id_ranges):
            ans += 1
    return ans


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    id_ranges, ids = parse_input(input_str)
    id_ranges = sorted(id_ranges)
    count = 0

    last_end = id_ranges[0][0] - 1
    for start, end in id_ranges:
        start = max(start, last_end + 1)
        count += max(0, end - start + 1)
        last_end = max(last_end, end)

    return count


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
