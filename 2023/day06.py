from utils import aoc_comm
import os
import math

# --- update day/ year for each challenge
settings = {
    'day' : 6,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions



def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    line1, line2 = inp_content
    line1 = line1[line1.find(':')+1:].strip()
    line2 = line2[line2.find(':')+1:].strip()

    return line1, line2



def solve_num_t(d, T):
    det = math.sqrt(T**2 - 4*(d+1))
    t1, t2 = (T-det)/2, (T+det)/2
    t1, t2 = math.ceil(t1), math.floor(t2)
    return t2-t1+1



@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    line1, line2 = parse_input(input_str)
    times = list(map(int, line1.split()))
    dists = list(map(int, line2.split()))

    ans = 1
    for T, d in zip(times, dists):
        ans *= solve_num_t(d, T)

    return ans




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    line1, line2 = parse_input(input_str)
    time = int(line1.replace(' ', ''))
    dist = int(line2.replace(' ', ''))

    return solve_num_t(dist, time)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
