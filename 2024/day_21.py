from utils import aoc_comm, run_example
import os

import itertools
from collections import Counter

# --- update day/ year for each challenge
settings = {
    'day' : 21,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''029A
980A
179A
456A
379A'''

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    return inp_content
    

def sanity_check_moves(moves, start_pos, get_ch):
    MOVE_TO_OFFSET = {
        '<' : (0, -1),
        '>' : (0, 1),
        'v' : (-1, 0),
        '^' : (1, 0),
        'A' : (0, 0)
    }
    x, y = start_pos
    typed_chars = []
    for ch in moves:
        ofx, ofy = MOVE_TO_OFFSET[ch]
        x, y = x + ofx, y + ofy
        cursor = get_ch(x, y)
        if cursor == '_':
            raise ValueError("Wrong directions")
        if ch == 'A':
            typed_chars.append(cursor)
    
    return ''.join(typed_chars)

NUM_PAD = '789456123_0A'
def num_keypad(ss):
    def get_coord(ch):
        pos = NUM_PAD.find(ch)
        x, y = divmod(pos, 3)
        return 3 - x, y
    
    def get_moves_opt(cur_pos, pos):
        offset = pos[0] - cur_pos[0], pos[1] - cur_pos[1]
        
        j_move = '<' if offset[1] < 0 else '>'
        i_move = 'v' if offset[0] < 0 else '^'

        mi = ''.join(i_move for _  in range(abs(offset[0])))
        mj = ''.join(j_move for _  in range(abs(offset[1])))
        
        op1 = mi + mj
        op2 = mj + mi
        moves_opt_both = [op1, op2] if op1!=op2 else [op1]
        
        if cur_pos[0] != 0 and pos[0] != 0:            
            moves_opt = moves_opt_both

        elif cur_pos[0] == 0:
            if pos[1] != 0:
                moves_opt = moves_opt_both
            else:
                moves_opt = [op1]
        else:
            if cur_pos[1] != 0:
                moves_opt = moves_opt_both
            else:
                moves_opt = [op2]

        return moves_opt
    
    
    cur_pos = get_coord('A')
    moves_opts = []
    for ch in ss:
        pos = get_coord(ch)
        moves_opts.append(get_moves_opt(cur_pos, pos))
        moves_opts.append(['A'])
        cur_pos = pos

    get_ch = lambda x,y : NUM_PAD[(3-x)*3 + y]
    all_moves = []
    for moves in itertools.product(*moves_opts):
        all_moves.append(''.join(moves))
        sanity_check_moves(all_moves[-1], get_coord('A'), get_ch)
    return all_moves

        



DIR_KEY_PAD = '_^A<v>'
def get_coord_dir_keypad(ch):
    pos = DIR_KEY_PAD.find(ch)
    x, y = divmod(pos, 3)
    x = 1 - x
    return x, y

def key_to_key_moves(key1, key2):
    cur_pos = get_coord_dir_keypad(key1)
    pos = get_coord_dir_keypad(key2)

    offset = pos[0] - cur_pos[0], pos[1] - cur_pos[1]
        
    j_move = '<' if offset[1] < 0 else '>'
    i_move = 'v' if offset[0] < 0 else '^'

    mj = ''.join(j_move for _  in range(abs(offset[1])))
    mi = ''.join(i_move for _  in range(abs(offset[0])))
    if cur_pos == (0, 0): # or pos == (0, 0)
        moves = mj + mi
        
    else:
        moves = mi + mj
    return moves



def dir_keypad(ss):
    moves = []
    last_ch = 'A'
    for ch in ss:
        moves.append(key_to_key_moves(last_ch, ch))
        moves.append('A')
        last_ch = ch
    return ''.join(moves)


VALID_DIR_KEYS = DIR_KEY_PAD.replace('_', '')
ALL_POSSIBLE_TRANSISTIONS = list(itertools.product(VALID_DIR_KEYS, VALID_DIR_KEYS))
MOVES_FOR_TRANSISITIONS = {
    transition:key_to_key_moves(*transition) for transition in ALL_POSSIBLE_TRANSISTIONS
}

# Insight from - https://www.reddit.com/r/adventofcode/comments/1hj2odw/comment/m3453er/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# Without this, the solution found isn't optimal
MOVES_FOR_TRANSISITIONS[('>','^')] = '<^'
MOVES_FOR_TRANSISITIONS[('^','>')] = 'v>'
MOVES_FOR_TRANSISITIONS[('A','v')] = '<v'
MOVES_FOR_TRANSISITIONS[('v','A')] = '^>'


def dir_pad_moves(moves, num):
    first_char = moves[0]
    transitions = list(zip(moves[:-1], moves[1:]))
    transitions.append(('A', first_char))
    cur_moves_ct = Counter(transitions)

    for _ in range(num):
        moves_to_counts = Counter()
        for tran, ct in cur_moves_ct.items():
            move_str = MOVES_FOR_TRANSISITIONS[tran]
            move_str = 'A' + move_str + 'A'

            new_transitions = list(zip(move_str[:-1], move_str[1:]))
            moves_to_counts.update({ nt: ct for nt in new_transitions})

        cur_moves_ct = moves_to_counts

    return sum(cur_moves_ct.values())


def solver(nums, compute_num_moves, num_bots):
    ans = 0
    for num in nums:
        all_moves = num_keypad(num)
        mn_len = None
        for moves in all_moves:
            ln = compute_num_moves(moves, num_bots)
            mn_len = min(mn_len or ln, ln)
        ans += int(num[:-1]) * mn_len
    return ans


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    nums = parse_input(input_str)
    def compute_num_moves(moves, num_bots):
        for _ in range(num_bots):
            moves = dir_keypad(moves)
        return len(moves)
    
    return solver(nums, compute_num_moves, num_bots=2)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    nums = parse_input(input_str)
    return solver(nums, dir_pad_moves, num_bots=25)
    

def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
