from utils import aoc_comm
import os
import functools

# --- update day/ year for each challenge
settings = {
    'day' : 8,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split('\n'):
        xx = ee.split(' | ')
        yield xx[0].split(), xx[1].split()


len_to_digit = {
    2: 1,
    3: 7,
    4: 4,
    7: 8
}


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    ans = 0
    for _, seq in inp:
        ans += sum(1 for disp in seq if len(disp) in len_to_digit)
    return ans


def get_num(disp: str, key_patterns: dict):
    nn = len(disp)
    digit = len_to_digit.get(nn, None)
    if digit is not None:
        return digit

    ss = set(disp)
    is_pattern_in_disp = lambda pat_s: len(key_patterns[pat_s] - ss) == 0
    if nn == 5:
        if is_pattern_in_disp('ACF'):
            return 3
        elif is_pattern_in_disp('EG'):
            return 2
        else:
            return 5
    elif nn == 6:
        if is_pattern_in_disp('ACF'):
            if is_pattern_in_disp('BD'):
                return 9
            else:
                return 0
        else:
            return 6


def identify_key_patterns(signals: list):
    len_to_pat = {}
    for sig in signals:
        if len(sig) in len_to_digit:
            len_to_pat[len(sig)] = set(sig)

    return {
        'ACF': len_to_pat[3],
        'EG': len_to_pat[7] - len_to_pat[4] - len_to_pat[3] - len_to_pat[2],
        'BD': len_to_pat[4] - len_to_pat[2]
    }


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    ans = 0
    for signals, seq in inp:
        get_num_p = functools.partial(get_num, key_patterns=identify_key_patterns(signals))
        num = int(''.join(str(dd) for dd in map(get_num_p, seq)))
        ans += num

    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
