from utils import aoc_comm
import os

settings = {
    'day' : 13,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    coord_lines, fold_lines = inp_content.strip().split('\n\n')
    coords = []
    for ee in coord_lines.split('\n'):
        x, y = ee.split(',')
        coords.append((int(y), int(x)))

    folds = []
    for ee in fold_lines.split('\n'):
        ee = ee.replace('fold along ', '').split('=')
        folds.append((1 if ee[0] == 'x'else 0, int(ee[1])))

    return coords, folds


def fold_mat(mat_coords, direction, val):
    ind = direction
    new_mat_coords = set()
    for coord in mat_coords:
        if coord[ind] < val:
            new_mat_coords.add(coord)
        else:
            new_coord = list(coord)
            new_coord[ind] = val - (coord[ind] - val)
            new_mat_coords.add(tuple(new_coord))

    mn_x = min(cord[0] for cord in new_mat_coords)
    mn_y = min(cord[1] for cord in new_mat_coords)

    mat_coords = new_mat_coords
    new_mat_coords = set()
    for cord in mat_coords:
        new_mat_coords.add((cord[0] - mn_x, cord[1] - mn_y))

    return new_mat_coords


def print_mat(mat):
    mx_x = max(cord[0] for cord in mat) + 1
    mx_y = max(cord[1] for cord in mat) + 1
    grid = [['.']*mx_y for _ in range(mx_x)]
    for cord in mat:
        grid[cord[0]][cord[1]] = '#'
    print('\n'.join( ''.join(row) for row in grid ))


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    coords, folds = parse_input(input_str)
    mat_coords = set(coords)

    for direction, val in folds[:1]:
        mat_coords = fold_mat(mat_coords, direction, val)

    return len(mat_coords)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    coords, folds = parse_input(input_str)
    mat_coords = set(coords)

    for direction, val in folds:
        mat_coords = fold_mat(mat_coords, direction, val)

    print_mat(mat_coords)
    return None


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
