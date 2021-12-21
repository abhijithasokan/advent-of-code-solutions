from utils import aoc_comm
import os
import functools
import itertools

settings = {
    'day' : 20,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    algo, img = inp_content.strip().split('\n\n')
    return algo, img.split('\n')


def get_surround_ind(ii, jj):
    shifts = itertools.product(range(-1, 2), range(-1, 2))
    coords = [(ii + x_shift, jj + y_shift) for x_shift, y_shift in shifts]
    return coords


def expand(img, exp_char, sz):
    n, m = len(img), len(img[0])
    pad_raw = exp_char * (m+2*sz)
    img2 = [pad_raw for _ in range(sz)]
    for ee in img:
        img2.append(exp_char*sz + ee + exp_char*sz)
    img2.extend([pad_raw for _ in range(sz)])
    return img2


def enhance(img, algo, exp_char):
    def translate(ii, img, algo, jj):
        xx = ''.join(img[xx][yy] for xx, yy in get_surround_ind(ii, jj))
        xx = xx.replace('#', '1').replace('.', '0')
        ind = int(xx, 2)
        return algo[ind]

    img2 = []
    for ii in range(1, len(img)-1):
        mp = functools.partial(translate, ii, img, algo)
        new_row = ''.join(map(mp, range(1, len(img[ii])-1)))
        img2.append(new_row)
    return expand(img2, exp_char, 2)


def solve(img, algo, cycles):
    exp = '.'
    img = expand(img, exp, 2)
    next_exp = {'.': algo[0], '#': algo[-1]}

    for _ in range(cycles):
        exp = next_exp[exp]
        img = enhance(img, algo, exp)
    return sum(row.count('#') for row in img)


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    algo, img = parse_input(input_str)
    return solve(img, algo, 2)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    algo, img = parse_input(input_str)
    return solve(img, algo, 50)


def main():
    l1_status = solve_l1()
    print(l1_status)
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
