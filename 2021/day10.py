from utils import aoc_comm
import os
from collections import defaultdict
from functools import reduce

# --- update day/ year for each challenge
settings = {
    'day' : 10,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split('\n'):
        yield ee


PAREN_PAIRS = [('(', ')'), ('[', ']'), ('<', '>'), ('{', '}')]
open_to_close = dict(PAREN_PAIRS)
close_to_open = {v: k for k, v in open_to_close.items()}


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    inp = parse_input(input_str)
    score = 0
    ch_to_score = dict([(')', 3), (']', 57), ('}', 1197), ('>', 25137)])
    for line in inp:
        stack = []
        for ch in line:
            if ch in open_to_close:
                stack.append(ch)
            else:
                expected_open = close_to_open[ch]
                open_char = stack.pop()
                if open_char != expected_open:
                    score += ch_to_score[ch]
                    break
    return score


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    scores = []
    ch_to_score = ch_to_score = dict([(')', 1), (']', 2), ('}', 3), ('>', 4)])
    for line in inp:
        stack = []
        for ch in line:
            if ch in open_to_close:
                stack.append(ch)
            else:
                expected_open = close_to_open[ch]
                open_char = stack.pop()
                if open_char != expected_open:
                    break
        else:
            closing_seq = map(open_to_close.__getitem__, stack[::-1])
            score = reduce(lambda total, close_ch: total*5 + ch_to_score[close_ch], closing_seq, 0)
            scores.append(score)

    scores.sort()
    ans = scores[len(scores)//2]
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
