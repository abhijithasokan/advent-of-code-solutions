from utils import aoc_comm
import os
import itertools
import collections

# --- update day/ year for each challenge
settings = {
    'day' : 21,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

CYCLE, WIN_SCORE1, WIN_SCORE2 = 10, 1000, 21
wrap_update = lambda val, inc: ((val + inc - 1) % CYCLE + 1)

def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    return tuple(map(lambda ss: int(ss[ss.rfind(':')+1:].strip()), inp_content))


def game(ps1, ps2):
    player, move = 0, 0
    pos, score = [ps1, ps2],  [0, 0]
    while score[0] < WIN_SCORE1 and score[1] < WIN_SCORE1:
        pos[player] = wrap_update(pos[player], (move*3+2) * 3)
        score[player] += pos[player]
        player = 1 - player
        move += 1
    return min(score) * (move*3)


OUTCOME_TO_POS = collections.Counter(map(sum, itertools.product(range(1, 4), range(1, 4), range(1, 4))))
def game2(key, memo_table = {}):
    if key in memo_table:
        return memo_table[key]

    turn, _scores, _poss = key
    scores, poss = list(_scores), list(_poss)
    player = (turn+1)%2

    ans = [0, 0]
    for move, chances in OUTCOME_TO_POS.items():
        old_pos = poss[player]

        poss[player] = wrap_update(old_pos, move)
        scores[player] += poss[player]

        if scores[player] >= WIN_SCORE2:
            ans[player] += chances
        else:
            tans = game2((turn+1, tuple(scores), tuple(poss)), memo_table)
            ans[0] += tans[0]*chances
            ans[1] += tans[1]*chances

        scores[player] -= poss[player]
        poss[player] = old_pos

    memo_table[key] = ans
    return ans


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    positions = parse_input(input_str)
    return game(*positions)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    positions = parse_input(input_str)
    return max(game2( (1, (0, 0), positions), {}))


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
