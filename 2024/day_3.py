from utils import aoc_comm, run_example
import os

import re
# --- update day/ year for each challenge
settings = {
    'day' : 3,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''

EXAMPLE_INP_2 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
'''

def parse_input(inp_content):
    inp_content = inp_content.strip()
    return inp_content
    # inp_content = inp_content.split('\n')
    # for line in inp_content:
    #     yield list(map(int, line.split()))
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    res = re.findall('mul\((\d+),(\d+)\)', inp)
    ans = 0
    for a,b in res:
        if len(a) > 3 or len(b) > 3:
            continue
        
        a, b = int(a), int(b)
        ans += a*b

    return ans



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    res = re.findall("mul\((\d+),(\d+)\)|(don't)|(do)", inp)
    ans = 0
    active = True
    for match in res:
        if match[2]:
            active = False
        elif match[3]:
            active = True
        elif active:
            a, b = match[:2]
            if len(a) > 3 or len(b) > 3:
                continue
            
            a, b = int(a), int(b)
            ans += a*b

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
