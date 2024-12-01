from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 15,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
import numpy as np
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split(','))
    yield from inp_content
    



def hash_func(ss):
    key = 0
    for ch in ss:
        key += ord(ch)
        key *= 17
        key %= 256
    return key

@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str)
    ans = 0
    for ee in inp:
        ans += hash_func(ee)

    return ans
    


from collections import OrderedDict
@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    box_to_lens = [OrderedDict() for _ in range(256)]
    for ee in inp:
        if '-' in ee:
            lens_label = ee[:ee.find('-')]
            box = hash_func(lens_label)
            box_to_lens[box].pop(lens_label, None)
        elif '=' in ee:
            lens_label, focal_len = ee.split('=')
            box = hash_func(lens_label)
            box_to_lens[box][lens_label] = int(focal_len)
        else:
            raise ValueError('Invalid input')

    '''rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1'''

    ans = 0
    for box, ee in enumerate(box_to_lens):
        for slot_ind, (lens_label, focal_len) in enumerate(ee.items()):
            ans += (box+1)*(slot_ind+1)*focal_len

    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
