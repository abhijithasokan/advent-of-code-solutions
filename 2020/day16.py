from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 16,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n\n')
    form, yt, ot = inp_content

    rules = {}
    xx = re.findall("([^:]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)", form)
    for ee in xx:
        name, a1, b1, a2, b2 = ee
        rules[name.strip()] = ( range(int(a1), int(b1)+1),  range(int(a2), int(b2)+1) )


    yt = list(map(int, yt.split('\n')[1].split(',')))

    nbt = []
    for ee in ot.split('\n')[1:]:
        nbt.append( list(map(int, ee.split(','))) ) 

    return (rules, yt, nbt)
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    rules, yt, nbt = parse_input(input_str)

    ans = 0
    for tic in nbt:
        for field in tic:
            if not any( (field in e1 or field in e2) for e1, e2 in rules.values()):
                ans += field
    return ans 


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    rules, yt, nbt = parse_input(input_str)

    new_nbt = []
    
    for tic in nbt:
        for field in tic:
            if not any( (field in e1 or field in e2) for e1, e2 in rules.values()):
                break
        else:
            new_nbt.append(tic)

    pos_to_valid_fields = {}
    for tic in new_nbt:
        for pos, field in enumerate(tic):
            valid_fields = []
            for rr, ee in rules.items():
                e1, e2 = ee
                if field in e1 or field in e2:
                    valid_fields.append(rr)
            if pos not in pos_to_valid_fields:
                pos_to_valid_fields[pos] = set(valid_fields)
            else:
                pos_to_valid_fields[pos] = pos_to_valid_fields[pos].intersection(valid_fields)

    heap = [(len(rrs), pos) for pos, rrs in pos_to_valid_fields.items()]
    import heapq
    heapq.heapify(heap)

    rule_to_valid_pos = defaultdict(list)
    for pos, rrs in pos_to_valid_fields.items():
        for rr in rrs:
            rule_to_valid_pos[rr].append(pos)

    visited = set()
    num_fields = len(yt)
    ans = 1
    while heap and (len(visited) != num_fields):
        priority, pos = heapq.heappop(heap)
        if pos in visited:
            continue
        assert(priority == 1)
        v_rules = pos_to_valid_fields[pos]
        assert(len(v_rules) == 1)
        rule = v_rules.pop()
        #print(pos, rule)
        visited.add(pos)
        for pp in rule_to_valid_pos[rule]:
            pos_to_valid_fields[pp].discard(rule)
            heapq.heappush(heap, ( len(pos_to_valid_fields[pp]), pp) )

        if "departure" in rule:
            ans *= yt[pos]
                           
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
