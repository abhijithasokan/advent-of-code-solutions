from utils import aoc_comm
import os

# --- update day/ year for each challenge
settings = {
    'day' : 1,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    for ee in inp_content:
        yield ee
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)

    ans = 0
    for ee in inp:
        digits = list(filter(lambda x: x is not None, map(lambda x: int(x) if x.isdigit() else None, ee)))
        ans += digits[0] *10 +  digits[-1]
    return ans 


def findfirst(ss, rev=False):
    digits_str = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    if rev:
        ss = ss[::-1]
        digits_str = [ee[::-1] for ee in digits_str]

    for ind in range(len(ss)):
        if ss[ind].isdigit():
            return int(ss[ind])
        for d, ds in enumerate(digits_str):
            if ss[ind:].startswith(ds):
                return d+1


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    ans = 0
    for ee in inp:
        d1 = findfirst(ee)
        d2 = findfirst(ee, True)
        ans += d1 *10 +  d2
    return ans 




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
