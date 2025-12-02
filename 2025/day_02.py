from utils import aoc_comm, run_example
import os
from typing import Callable, Iterable

# --- update day/ year for each challenge
settings = {
    "day": 2,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split(",")
    for line in inp_content:
        yield tuple(map(int, line.split("-")))


def solve(inp: Iterable, validator: Callable[[str], bool]) -> int:
    ans = 0
    for first_id, last_id in inp:
        for ii in range(first_id, last_id + 1):
            if validator(str(ii)):
                ans += int(ii)
    return ans


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    is_invalid = lambda s: (len(s) % 2 == 0) and (s[: len(s) // 2] == s[len(s) // 2 :])
    return solve(parse_input(input_str), is_invalid)


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    ans = 0

    def is_invalid(s):
        n = len(s)
        for l in range(1, n // 2 + 1):
            rep_count, rem = divmod(n - l, l)
            prefix = s[:l]
            if rem == 0 and prefix * rep_count == s[l:]:
                return True
        return False

    return solve(parse_input(input_str), is_invalid)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
