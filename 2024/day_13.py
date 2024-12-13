from utils import aoc_comm, run_example
import os

import re
import numpy as np

from ortools.linear_solver import pywraplp


# --- update day/ year for each challenge
settings = {
    'day' : 13,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip()
    res = re.findall('Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)', inp_content)
    for mt in res:
        # print(mt)
        yield {
            'A' : np.array([int(mt[0]), int(mt[1])]),
            'B' : np.array([int(mt[2]), int(mt[3])]),
            'T' : np.array([int(mt[4]), int(mt[5])]),
        }
    

def solve_2d_linear_equation_for_integer_solutions(X, y):
    det = X[0][0]*X[1][1] - X[0][1]*X[1][0]

    mm = np.array([
        [X[1][1], - X[0][1]],
        [-X[1][0], X[0][0]]
    ])

    res = np.divmod(mm @ y, det)
    
    if all(res[1] == 0):
        return res[0]
    return None


def solve(inp, offest=0):
    ans = 0
    cost = np.array([3, 1])
    for game_data in inp:
        y = game_data['T'] + np.array([offest, offest])
        X = np.array([game_data['A'], game_data['B']]).T
        w = solve_2d_linear_equation_for_integer_solutions(X, y)
        if w is not None:
            ans += w @ cost

    return ans



@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    return solve(inp)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    return solve(inp, offest=10000000000000)
    

def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
