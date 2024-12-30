from utils import aoc_comm, run_example
import os

import itertools
import functools

# --- update day/ year for each challenge
settings = {
    'day' : 7,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    for line in inp_content:
        res, operands = line.split(': ')
        res = int(res)
        operands = list(map(int, operands.strip().split()))
        yield res, operands
    

OPS = {
    '*' : lambda x,y: x*y, 
    '+' : lambda x,y: x+y,
    '||' : lambda x,y: int(str(x)+str(y))
}


def is_solvable(res, operands, operator_choices):
    reducer = lambda last_res, cur_ops: OPS[cur_ops[0]](last_res, cur_ops[1])
    num_ops = len(operands) - 1
    for ops in itertools.product(*[operator_choices for _ in range(num_ops)]):
        cur_res = functools.reduce(reducer, zip(ops, operands[1:]), operands[0])
        if cur_res == res:
            return True
    return False

    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    ans = 0
    for res, operands in inp:
        if is_solvable(res, operands, ['*', '+']):
            ans += res
    return ans


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    ans = 0
    for res, operands in inp:
        if is_solvable(res, operands, ['*', '+', '||']):
            ans += res
    return ans


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
