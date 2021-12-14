from utils import aoc_comm
import os
from collections import Counter, defaultdict

settings = {
    'day' : 14,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    seq, pairs = inp_content.strip().split('\n\n')
    pair_map = dict(tuple(ee.split(' -> ')) for ee in pairs.split('\n'))
    return seq, pair_map


def func(seq, pair_map, cycle_count):
    pairs_to_count = Counter(seq[ind:ind+2] for ind in range(len(seq)-1))
    for _ in range(cycle_count):
        pairs_to_count_new = defaultdict(int)
        for pr, cc in pairs_to_count.items():
            mid_char = pair_map[pr]
            pr1, pr2 = pr[0] + mid_char, mid_char + pr[1]
            pairs_to_count_new[pr1] += cc
            pairs_to_count_new[pr2] += cc
        pairs_to_count = pairs_to_count_new

    cc = Counter([seq[0], seq[-1]])
    for pr, ct in pairs_to_count.items():
        cc[pr[0]] += ct
        cc[pr[1]] += ct

    ans = cc.most_common()[0][1]//2 - cc.most_common()[-1][1]//2
    return ans


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    seq, pair_map = parse_input(input_str)
    return func(seq, pair_map, 10)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    seq, pair_map = parse_input(input_str)
    return func(seq, pair_map, 40)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
