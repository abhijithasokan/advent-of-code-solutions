import functools

from utils import aoc_comm
import os
import itertools
import heapq
import operator

# --- update day/ year for each challenge
settings = {
    'day' : 9,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split('\n'):
        yield [int(e) for e in ee]


def get_surround_ind(ii, jj, r_sz, c_cz, incl_diagonals = True):
    shifts = itertools.product(range(-1, 2), range(-1, 2))
    if incl_diagonals:
        coords = [ (ii + x_shift, jj + y_shift) for x_shift, y_shift in shifts if not (x_shift == y_shift == 0) ]
    else:
        coords = [(ii + x_shift, jj + y_shift) for x_shift, y_shift in shifts if (x_shift == 0 or y_shift == 0) and (x_shift != y_shift)]
    return filter(lambda coord: (coord[0] in range(r_sz) and coord[1] in range(c_cz)), coords)


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    matrix = list(parse_input(input_str))
    ans = 0
    r_sz, c_cz = len(matrix), len(matrix[0])
    for ii, jj in itertools.product(range(r_sz), range(c_cz)):
        if all(matrix[ii][jj] < matrix[x][y] for x, y in get_surround_ind(ii, jj, r_sz, c_cz, True)):
            ans += matrix[ii][jj] + 1
    return ans


def flood_fill(matrix, ii, jj, r_sz, c_cz):
    if matrix[ii][jj] == -1 or matrix[ii][jj] == 9:
        return 0
    else:
        matrix[ii][jj] = -1
        pans = 1
        for x, y in get_surround_ind(ii, jj, r_sz, c_cz, False):
            pans += flood_fill(matrix, x, y, r_sz, c_cz)
        return pans


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    matrix = list(parse_input(input_str))
    r_sz, c_cz = len(matrix), len(matrix[0])
    top_basins = []
    for ii, jj in itertools.product(range(r_sz), range(c_cz)):
        heapq.heappush(top_basins, flood_fill(matrix, ii, jj, r_sz, c_cz))
        if len(top_basins) > 3:
            heapq.heappop(top_basins)
    ans = functools.reduce(operator.mul, top_basins)
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
