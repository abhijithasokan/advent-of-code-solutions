from utils import aoc_comm
import os
import itertools

# --- update day/ year for each challenge
settings = {
    'day' : 11,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    matrix = [list(map(int, ss)) for ss in inp_content.split('\n')]
    return matrix, len(matrix), len(matrix[0])


def get_surround_ind(ii, jj, r_sz, c_cz):
    shifts = itertools.product(range(-1, 2), range(-1, 2))
    coords = [(ii + x_shift, jj + y_shift) for x_shift, y_shift in shifts if not (x_shift == y_shift == 0) ]
    return filter(lambda coord: (coord[0] in range(r_sz) and coord[1] in range(c_cz)), coords)


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    matrix, nn, mm = parse_input(input_str)
    tot_flash_count = 0

    for _ in range(100):
        highs = set()
        for ii, jj in itertools.product(range(nn), range(mm)):
            matrix[ii][jj] += 1
            if matrix[ii][jj] > 9:
                highs.add((ii, jj))
        flash_count = 0
        visited = set()
        while highs:
            new_highs = set()
            for ii, jj in highs:
                if (ii, jj) in visited:
                    continue
                matrix[ii][jj] = 0
                flash_count += 1
                visited.add((ii, jj))
                for cx, cy in get_surround_ind(ii, jj, nn, mm):
                    if (cx, cy) not in visited:
                        matrix[cx][cy] += 1
                        if matrix[cx][cy] > 9:
                            new_highs.add((cx, cy))
            highs = new_highs
        tot_flash_count += flash_count

    return tot_flash_count


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    matrix, nn, mm = parse_input(input_str)
    cycle = 0
    while True:
        cycle += 1
        highs = set()
        for ii, jj in itertools.product(range(nn), range(mm)):
            matrix[ii][jj] += 1
            if matrix[ii][jj] > 9:
                highs.add((ii, jj))
        flash_count = 0
        visited = set()
        while highs:
            new_highs = set()
            for ii, jj in highs:
                if (ii, jj) in visited:
                    continue
                matrix[ii][jj] = 0
                flash_count += 1
                visited.add((ii, jj))
                for cx, cy in get_surround_ind(ii, jj, nn, mm):
                    if (cx, cy) not in visited:
                        matrix[cx][cy] += 1
                        if matrix[cx][cy] > 9:
                            new_highs.add((cx, cy))
            highs = new_highs
        if flash_count == nn*mm:
            return cycle


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
