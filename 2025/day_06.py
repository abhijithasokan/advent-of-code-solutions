from functools import reduce
from hmac import new
import operator
from turtle import st
from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    "day": 6,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content, stage: int = 1):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    operators = inp_content[-1].strip().split()

    if stage == 1:
        matrix = []
        for line in inp_content[:-1]:
            matrix.append(list(map(int, line.strip().split())))
        nn = len(matrix)
        operands = [
            [matrix[ii][ind] for ii in range(nn)] for ind in range(len(operators))
        ]
        return operators, operands

    elif stage == 2:
        opr_lines = inp_content[:-1]
        n, m = len(opr_lines), len(opr_lines[0])
        new_operands = []
        rot_opr_lines = []
        for j in range(m):
            new_line = ""
            for i in range(n):
                new_line += opr_lines[i][j]
            if new_line.strip() == "":
                new_operands.append(rot_opr_lines)
                rot_opr_lines = []
            else:
                rot_opr_lines.append(int(new_line))

        new_operands.append(rot_opr_lines)
        return operators, new_operands


def solve(operands, operators):
    ans = 0
    op_map = {"*": operator.mul, "+": operator.add}

    for ind, op in enumerate(operators):
        ans += reduce(op_map[op], operands[ind])
    return ans


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    operators, matrix = parse_input(input_str, stage=1)
    return solve(matrix, operators)


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    operators, operands = parse_input(input_str, stage=2)
    return solve(operands, operators)


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
