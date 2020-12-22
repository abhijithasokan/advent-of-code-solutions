from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 22,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n\n')
    p1, p2 = inp_content
    p1, p2 = p1.split('\n')[1:], p2.split('\n')[1:]
    return list(map(int, p1))[::-1], list(map(int, p2))[::-1]



def game_l1(p1, p2):
    while p1 and p2:
        if p1[-1] > p2[-1]:
            card1 = p1.pop()
            card2 = p2.pop()
            p1 = [card2, card1] + p1
        else:
            card1 = p1.pop()
            card2 = p2.pop()
            p2 = [card1, card2] + p2
    return p1, p2

def get_final_num(pp):
    return sum( (ind + 1) * ee for ind, ee in enumerate(pp)  )

@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    p1, p2 = parse_input(input_str)
    p1, p2 = game_l1(p1, p2)
    return get_final_num(p1 or p2) 



def check_cache(keyy, memo_table):
    if keyy in memo_table:
        print("cache hit")
        return memo_table[keyy]

    keyy = keyy[::-1]
    if keyy in memo_table:
        print("flip cache hit")
        return 1 - memo_table[keyy]
    return None


import copy
def game_l2(p1, p2, memo_table, sub = True):
    if sub:
        max_card1 = max(p1)
        max_card2 = max(p2)
        if max_card1 > max_card2  and ( max_card1 > (len(p1) + len(p2)-2) ):
            return 1, None, None

    cache_table_key = (tuple(p1), tuple(p1))
    cache_entry = check_cache(cache_table_key, memo_table)
    
    if cache_entry is not None:
        return cache_entry, None, None
    
    seen_deck1, seen_deck2 = set(), set()

    intermediate_states = []
    while p1 and p2:
        deck1 = tuple(p1)
        deck2 = tuple(p2)
        
        if deck1 in seen_deck1 or deck2 in seen_deck2:
            final_winner = 1
            memo_table[cache_table_key] = final_winner
            return final_winner, None, None

        seen_deck1.add(deck1)
        seen_deck2.add(deck2)
        intermediate_state = (deck1, deck2)
        intermediate_states.append(intermediate_state)

        cache_entry = check_cache(intermediate_state, memo_table)    
        if cache_entry is not None:
            return cache_entry, None, None
        
        if p1[-1] <= (len(p1)-1) and p2[-1] <= (len(p2)-1):
            len1 = p1[-1]
            len2 = p2[-1]
            new_p1, new_p2  = copy.deepcopy(p1), copy.deepcopy(p2)
            new_p1.pop(), new_p2.pop()
            winner, _ ,_  = game_l2( new_p1[-len1:], new_p2[-len2:], memo_table)
        else:
            winner = 1 if p1[-1] > p2[-1] else 0
            
        if winner == 1:
            card1 = p1.pop()
            card2 = p2.pop()
            p1 = [card2, card1] + p1
        else:
            card1 = p1.pop()
            card2 = p2.pop()
            p2 = [card1, card2] + p2
            
    final_winner = 1 if len(p1) else 0
    for state in intermediate_states:
        memo_table[state] = final_winner
        state = state[::-1]
        memo_table[state] = 1 - final_winner
        
    return final_winner, p1, p2
    
@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    p1, p2 = parse_input(input_str)
    winner, p1, p2 = game_l2(p1, p2, {}, False)
    return get_final_num(p1 if winner == 1 else p2)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
