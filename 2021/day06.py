from utils import aoc_comm
import os

# --- update day/ year for each challenge
settings = {
    'day' : 6,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split(','):
        yield int(ee)

memo = {}
def find_num_fish(clock, days):
    key = clock, days
    cached_ans =  memo.get(key, None)
    if cached_ans is not None:
        return cached_ans

    if days == 0:
        return 0

    if clock == 0:
        ans = 1 + find_num_fish(6, days-1) + find_num_fish(8, days-1)
    else:
        ans = find_num_fish(clock-1, days-1)

    memo[key] = ans
    return ans

def calc_population(inp, days):
    ans = 0
    for time in inp:
        ans += (1 + find_num_fish(time, days))
    return ans

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string
    global memo
    memo = {}
    return calc_population(parse_input(input_str), 80)

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    memo = {}
    return calc_population(parse_input(input_str), 256)



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
