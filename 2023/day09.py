from utils import aoc_comm
import os

# --- update day/ year for each challenge
settings = {
    'day' : 9,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    for line in inp_content:
        yield list(map(int, line.strip().split()))


def diff(series):
    return list(map(lambda x: x[1]-x[0], zip(series[:-1], series[1:])))


def solve(input_str, rev_series = False):
    inp = parse_input(input_str)

    ans = 0 
    for series in inp:
        series = series[::-1] if rev_series else series
        last_items = []

        while any(series):
            last_items.append(series[-1])
            series = diff(series)
    
        prediction = sum(last_items)
        ans += prediction
    
    return ans


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    return solve(input_str)
    

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    return solve(input_str, rev_series=True)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
