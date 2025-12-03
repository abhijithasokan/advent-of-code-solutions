from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    "day": 3,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """987654321111111
811111111111119
234234234234278
818181911112111
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    for line in inp_content:
        yield list(map(int, line))


def solve(inp, digit_count: int):
    def func(nums):
        res = 0
        for rem in reversed(range(digit_count)):
            ind = min(range(len(nums) - rem), key=lambda ii: (-nums[ii], ii))
            res = res * 10 + nums[ind]
            nums = nums[ind + 1 :]
        return res

    ans = 0
    for nums in inp:
        ans += func(nums)

    return ans


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)
    return solve(inp, 2)


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)
    return solve(inp, 12)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
