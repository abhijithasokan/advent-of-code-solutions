from utils import aoc_comm
import os

# --- update day/ year for each challenge
settings = {
    'day' : 7,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    for line in inp_content:
        hand, bid = line.strip().split()
        yield hand, int(bid)

from collections import Counter

ORDERING = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
KEY_MAP = {v: k for k,v in enumerate(ORDERING[::-1])}

def get_key(hand, hand_orig=None, KEY_MAP=KEY_MAP):
    hand_orig = hand_orig or hand
    cc = Counter(hand)
    counts = tuple(sorted(cc.values(), reverse=True))
    hand_mapped = tuple(KEY_MAP[ee] for ee in hand_orig)
    return (counts, hand_mapped)
    

def get_key2(hand):
    hand2 = hand
    if 'J' in hand:
        cc = Counter(hand)
        for card, _ in cc.most_common():
            if card != 'J':
                hand2 = hand.replace('J', card)
                break
    
    KEY_MAP2 = KEY_MAP.copy()
    KEY_MAP2['J'] = -1
    return get_key(hand2, hand, KEY_MAP2)


def solve(input_str, key_func):
    inp = list(parse_input(input_str))

    arranged = sorted(inp, key=lambda x: key_func(x[0]))
    rank_and_bid = [(ind+1, bid) for ind, (_, bid) in enumerate(arranged)]
    ans = sum(x[0]*x[1] for x in rank_and_bid)
    return ans


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    return solve(input_str, get_key)
    

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    return solve(input_str, get_key2)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
