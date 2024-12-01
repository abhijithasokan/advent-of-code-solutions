from utils import aoc_comm
import os

# --- update day/ year for each challenge
settings = {
    'day' : 10,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    start_pos = (0,0)
    for ii, line in enumerate(inp_content):
        jj = line.find('S')
        if jj != -1:
            start_pos = (ii, jj)
            break

    return inp_content, start_pos


import itertools
def surrounding_indices(mat, ii, jj):
    n, m = len(mat), len(mat[0])
    ii_s = [ii]
    if ii != 0:
        ii_s.append(ii-1)
    if ii != n-1:
        ii_s.append(ii+1)

    jj_s = [jj]
    if jj != 0:
        jj_s.append(jj-1)
    if jj != m-1:
        jj_s.append(jj+1)

    inidices = list(itertools.product(ii_s, jj_s))
    inidices.remove((ii, jj))
    return inidices



ENTRY_MOVEMENT_MAP = {
    '|' : [(1, 0), (-1, 0)],
    '-' : [(0, 1), (0, -1)],
    'L' : [(1, 0), (0, -1)],
    'J' : [(1, 0), (0, 1)], 
    '7' : [(-1, 0), (0, 1)],
    'F' : [(-1, 0), (0, -1)],
    '.' : [],
}

def negate(tup):
    return tuple(-x for x in tup)

EXIT_MOVEMENT_MAP = {
    k : [negate(mm) for mm in v] for k, v in ENTRY_MOVEMENT_MAP.items()
}


def walk(start_pos, mat):
    cur_i, cur_j = start_pos

    steps = 0
    poly_points = []
    poly_points.append(start_pos)
    vert_moves = set()
    for ii, jj in surrounding_indices(mat, cur_i, cur_j):
        move = (ii - cur_i, jj - cur_j)
        pipe = mat[ii][jj]
        if move in ENTRY_MOVEMENT_MAP[pipe]:
            cur_i, cur_j = ii, jj
            steps += 1
            if move[0] == 1:
                vert_moves.add((cur_i-1, cur_j))
            elif move[0] == -1:
                vert_moves.add((cur_i, cur_j))
            break

    last_move = move

    while mat[cur_i][cur_j] != 'S':
        pipe = mat[cur_i][cur_j]
        poly_points.append((cur_i, cur_j))
        possible_entries = ENTRY_MOVEMENT_MAP[pipe]
        exit_move = negate(possible_entries[1 - possible_entries.index(last_move)])
        cur_i, cur_j = cur_i + exit_move[0], cur_j + exit_move[1]
        steps += 1
        last_move = exit_move

        if exit_move[0] == 1:
            vert_moves.add((cur_i-1, cur_j))
        elif exit_move[0] == -1:
            vert_moves.add((cur_i, cur_j))

    return steps, poly_points, vert_moves


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    mat, start_pos = parse_input(input_str)
    moves, _, _ = walk(start_pos, mat)
    return moves//2


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    mat, start_pos = parse_input(input_str)
    _, poly_points, vert_moves = walk(start_pos, mat)
    n, m = len(mat), len(mat[0])

    poly_points = set(poly_points)

    inside_points_count = 0
    points_to_leftside = [[0]*m for _ in range(n)]
    for ii, jj in itertools.product(range(0, n), range(0, m)):
        points_to_leftside[ii][jj] = points_to_leftside[ii][jj-1] if jj > 0 else 0
        if (ii, jj) in poly_points:
            if (ii, jj) in vert_moves:
                points_to_leftside[ii][jj] += 1
            continue

        if points_to_leftside[ii][jj] % 2: # refer your graphics lecture - rasterization
            inside_points_count += 1

    return inside_points_count




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
