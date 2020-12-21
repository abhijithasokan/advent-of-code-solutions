from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 21,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


from collections import Counter, defaultdict
import operator

def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    for ee in inp_content:
        ingrediants, allergents = ee.split('(contains ')
        ingrediants = ingrediants.strip().split()
        allergents = allergents.replace(')','').replace(',','').strip().split()
        yield ingrediants, allergents


def remove_item(name, rev_map, food_list, ind):
    for food_ind in rev_map[name]:
        food_list[food_ind][ind].discard(name)
    del rev_map[name]


def get_ingrediant_allergent_mapping(inp):
    food_list = []
    rev_map_for_ingrediants = defaultdict(list)
    rev_map_for_allergents = defaultdict(list)
    all_allergents = []
    
    for ingrediants, allergents in inp:
        food_list.append( (set(ingrediants), set(allergents) )  )
        all_allergents.extend(allergents)
        food_ind = len(food_list) - 1
        for ee in food_list[-1][0]:
            rev_map_for_ingrediants[ee].append(food_ind)

        for ee in food_list[-1][1]:
            rev_map_for_allergents[ee].append(food_ind)

    map_allergent_to_common_ings = {}
    all_allergents = set(all_allergents)    
    
    for allergent in all_allergents:
        common_ings = None
        for food_ind in rev_map_for_allergents[allergent]:
            common_ings = common_ings & food_list[food_ind][0] if common_ings else  food_list[food_ind][0]
        map_allergent_to_common_ings[allergent] = common_ings or set()

    queue = []
    
    min_allergent = min(map_allergent_to_common_ings.items(), key = lambda item: len(item[1]) )[0]
    assert(len(map_allergent_to_common_ings[min_allergent]) == 1)
    queue.append(min_allergent)

    final_mapping = {}
    while queue:
        min_allergent = queue.pop()
        min_allergent_ings = map_allergent_to_common_ings[min_allergent]

        if not min_allergent_ings:
            continue
        match_ing = min_allergent_ings.pop()
        final_mapping[match_ing] = min_allergent
        for allergent, ings in map_allergent_to_common_ings.items():
            ings.discard(match_ing)
            if len(ings) == 1:
                queue.append(allergent)
            remove_item(match_ing, rev_map_for_ingrediants, food_list, 0)

    return final_mapping, rev_map_for_ingrediants



@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str)
    _, rev_map_for_ingrediants = get_ingrediant_allergent_mapping(inp)
    ans = sum(len(ee) for ee in rev_map_for_ingrediants.values())
    return ans
          

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    final_mapping, _ = get_ingrediant_allergent_mapping(inp)
    ans = ','.join( item[0] for item in sorted(final_mapping.items(), key = operator.itemgetter(1)) )
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
