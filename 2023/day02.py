from utils import aoc_comm
import os
import re
import functools
import operator

# --- update day/ year for each challenge
settings = {
    'day' : 2,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green'''

    color_to_pos = {'red' : 0, 'green': 1, 'blue' : 2}
    def to_list(ss):
        ll = [0, 0, 0]
        for ee in ss.split(','):
            ee = ee.strip()
            num, color = ee.split(' ')
            ll[color_to_pos[color]] = int(num)
        return ll


    inp_content = inp_content.strip().split('\n')
    for ee in inp_content:
        srch = re.search('Game (\d+): (.+)', ee, re.DOTALL)
        game = int(srch.group(1))
        reads = [to_list(ee) for ee in srch.group(2).split(';')]
        yield game, reads

    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)

    lims = [12, 13, 14]
    ans = 0
    for ee in inp:
        game_id, reads = ee
        if all( all(a<=b for (a,b) in zip(rd, lims)) for rd in reads):
            ans += game_id
    return ans 




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    lims = [12, 13, 14]
    ans = 0
    for ee in inp:
        _, reads = ee
        colorwise_counts = list(zip(*reads))
        min_count = map(max, colorwise_counts)
        ans += functools.reduce(operator.mul, min_count)
        
    return ans 




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
