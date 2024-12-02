from utils import aoc_comm, run_example
import os

from collections import Counter

# --- update day/ year for each challenge
settings = {
    'day' : None,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP = '''
'''

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    for line in inp_content:
        yield list(map(int, line.split()))
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    return None



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    return None



def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
