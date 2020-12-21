from utils import aoc_comm
import os
import re

settings = {
    'day' : 20,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

from collections import Counter, defaultdict
import math
import functools
import itertools
import copy

def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n\n')
    for ee in inp_content:
        ee = ee.split('\n')
        num, matrix = ee[0], ee[1:]
        num = int(num.replace('Tile','').replace(':','').strip())
        yield num, matrix

def build_sides(matrix):
    _top = matrix[0]
    _bot = matrix[-1]
    _left = ''.join(matrix[ii][0] for ii in range(len(matrix)) )
    _right = ''.join(matrix[ii][-1] for ii in range(len(matrix)) )
    return  { 'bot' : _bot,  'right': _right, 'top' : _top, 'left' : _left }

def rev(st):
    return str(st[::-1])

def rotate_side(sides, rot): 
    rot = (rot  + 4) % 4
    if rot == 0:
        return sides
    sides = rotate_side(sides, rot - 1)
    return { 'top' : rev(sides['left']), 'right' : sides['top'], 'bot' : rev(sides['right']), 'left' : sides['bot'] }


def flip_side_horizotal(sides):
    return { 'bot' : sides['top'], 'top' : sides['bot'], 'left' : rev(sides['left']), 'right' : rev(sides['right']) }


def flip_side_vertical(sides):
    return { 'left' : sides['right'], 'right' : sides['left'], 'top' : rev(sides['top']), 'bot' : rev(sides['bot']) }


def flip_mat_vertical(matrix):
    return [ ee[::-1] for ee in matrix]

def flip_mat_horizontal(matrix):
    return matrix[::-1]

def rotate_mat(arr, rot):
    rot = (rot + 4) % 4
    if rot == 0:
        return arr
    arr = rotate_mat(arr, rot - 1)
    arr = [ ''.join(arr[ii][jj] for ii in range(len(arr)-1,-1,-1) ) for jj in range(len(arr[0]))   ]
    return arr


def iter_possible_sides(cur_sides):
    seen_states = set()
    for rot in range(4):
        for h_flip, v_flip in itertools.product([False, True], [False, True]):
            sides = cur_sides
            sides = flip_side_horizotal(sides) if h_flip else sides
            sides = flip_side_vertical(sides) if v_flip else sides

            tup_side = convert_to_tuple(sides)
            if tup_side in seen_states:
                continue
            yield sides, tup_side, (rot, h_flip, v_flip)
            seen_states.add(tup_side)

        cur_sides = rotate_side(cur_sides, 1)

        
ORDER_OF_SIDES = ['bot', 'right', 'top', 'left']
DIRECTION_KEY_MAP = dict( enumerate(ORDER_OF_SIDES) )


def convert_to_tuple(sides):
    return tuple( sides[dir_name] for dir_name in ORDER_OF_SIDES )


def get_solved_grid(inp):
    mat_map = {}
    ind_to_sides = {}
    connect_map = { direction : defaultdict(list) for direction in ORDER_OF_SIDES }

    int_to_state_to_conf = {}
    for ind, matrix in inp:
        mat_map[ind] = matrix
        orig_sides = build_sides(matrix) 
        ind_to_sides[ind] = orig_sides
        conf_dict = int_to_state_to_conf[ind] = {}
        for side_d, cf_key, conf in iter_possible_sides(orig_sides):
           conf_dict[cf_key] = conf
           for dir_name, side in side_d.items():
               connect_map[dir_name][side].append( (ind, side_d) )


    sz = int(math.sqrt(len(ind_to_sides)))

    visited = set()
    for ind, orig_sides in ind_to_sides.items():
        found = False
        grid = [ [ [None, None] ]*sz for _ in range(sz) ]
        visited.add(ind)
        for sides, _, _ in iter_possible_sides(orig_sides):
            grid[0][0] = (ind, sides)
            if try_all(grid, 1, connect_map, visited, sz):
                found = True
                break
            
        if found:
            break

        visited.discard(ind)

    assert(found)
    return grid, mat_map, int_to_state_to_conf
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str)
    grid, _, _ = get_solved_grid(inp)
    ans = grid[0][0][0] * grid[-1][-1][0] * grid[0][-1][0] * grid[len(grid)-1][0][0]
    return ans 
    
def get_new_grid(dim):
    return [ [ [None, None] ]*dim for _ in range(dim) ]


def get_matching_matrices_1d(dir1, dir2, connect_map, visited, sides):
    #give all possible mat that can connect to `sides[dir2]` from `dir1` direction
    for ind, other_sides in filter(lambda xx: xx[0] not in visited,  connect_map[dir1][sides[dir2]] ):
        yield ind, other_sides
    
def get_matching_matrices_2d(vdir, hdir, connect_map, visited, sides1, sides2):
    ot_hdir = 'leftright'.replace(hdir, '')
    ot_vdir = 'topbot'.replace(vdir, '')

    # get all possible mat that connects to sides1[] via `vdir` and sides2[] via `hdir` 
    for ind1, other_sides1 in get_matching_matrices_1d(hdir, ot_hdir, connect_map, visited, sides2):
        for ind2, other_sides2 in get_matching_matrices_1d(vdir, ot_vdir, connect_map, visited, sides1):
            if ind1 == ind2 and other_sides1 == other_sides2:
                yield ind1, other_sides1

    return None
 
def try_all(grid, batch, connect_map, visited, sz):
    _, last_corner_sides = grid[batch-1][batch-1] 

    if batch == sz:
        return True
    
    for ind1, sides1 in get_matching_matrices_1d('left', 'right', connect_map, visited, last_corner_sides):
        grid[batch-1][batch] = ind1, sides1 # right
        visited.add(ind1)

        for ind2, sides2 in get_matching_matrices_1d('top', 'bot', connect_map, visited, last_corner_sides):
            grid[batch][batch-1] = ind2, sides2 # from bot 
            visited.add(ind2)

            for ind3, new_corner_sides in get_matching_matrices_2d('top', 'left', connect_map, visited, sides1, sides2):
                grid[batch][batch] = ind3, new_corner_sides
                visited.add(ind3)

                visited_deep = copy.deepcopy(visited)
                if direction_fill(grid, batch, connect_map, visited_deep, 'horizontal'):
                    if direction_fill(grid, batch, connect_map, visited_deep, 'vertical'):
                        if try_all(grid, batch + 1, connect_map, visited_deep, sz):
                            return True

                visited.discard(ind3)
            visited.discard(ind2)     
        visited.discard(ind1)

    return False

def direction_fill(grid, batch, connect_map, visited, direction = 'vertical'):
    row = batch
    col = batch
    col_dec, row_dec = 0, 0
    side_dir1, side_dir2 = None, None
    if direction == 'horizontal':
        col_dec = 1
        side_dir1, side_dir2 = 'top', 'right'
        col -= 1
    else:
        row_dec = 1
        side_dir1, side_dir2 = 'bot', 'left'
        row -= 1

    status = progress_direction(grid, side_dir1, side_dir2, connect_map, visited, row, col, row_dec, col_dec)
    return status


def progress_direction(grid, side_dir1, side_dir2, connect_map, visited, row, col, row_dec, col_dec):
    _, last_sides = grid[row][col]
    row -= row_dec
    col -= col_dec
    if row < 0 or col < 0:
        return True
    
    adj_side, last_sides = grid[row-col_dec][col-row_dec][1], last_sides
    if row_dec: # moving vertically
        adj_side, last_sides = last_sides, adj_side
    for ind, sides in get_matching_matrices_2d(side_dir1, side_dir2, connect_map, visited, adj_side, last_sides):
        visited.add(ind)
        grid[row][col] = ind, sides
        if progress_direction(grid, side_dir1, side_dir2, connect_map, visited, row, col, row_dec, col_dec):
            return True
        visited.discard(ind)

    return False
        
    
                
@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)

    grid, mat_map, int_to_state_to_conf = get_solved_grid(inp)
        
    image =  build_image(grid, mat_map, int_to_state_to_conf)
    monster_mat = ['                  # ', '#    ##    ##    ###', ' #  #  #  #  #  #   ']
    ans = calc_water_roughness(image, monster_mat)
    return ans 


def poss_monters(mons_mat):
    for rot in range(4):
        for h_flip, v_flip in itertools.product([False, True], [False, True]):
            mat = mons_mat
            mat = flip_mat_horizontal(mat) if h_flip else mat
            mat = flip_mat_vertical(mat) if v_flip else mat
            yield mat
        mons_mat = rotate_mat(mons_mat, 1)


def indices_of_char(mat, char):
    indices = []
    for row in mat:
        row_indices = []
        for ind, ch in enumerate(row):
            if ch == char:
                row_indices.append(ind)
        indices.append(row_indices)
    return indices

def transform_indices_to_cord(x_cord, y_cord, indices):
    cords = []
    for row, indices in enumerate(indices):
        cords.extend( (row + x_cord, ind + y_cord) for ind in indices  )
    return cords

        
def calc_water_roughness(image, mons_mat):
    seen_states = set()
    for mat in poss_monters(mons_mat):
        state = ''.join(mat)
        if state in seen_states:
            continue
        seen_states.add(state)
        nn, mm = len(mat), len(mat[0])
    
        indices = indices_of_char(mat, '#')
        used_indices = set()
        for ii in range(len(image) - nn):
            for jj in range(len(image[0]) - mm):
                trans_indices = transform_indices_to_cord(ii, jj, indices)
                if all( image[x][y] == '#' for x,y in trans_indices ):  # monster fits perfectly
                    used_indices.update(trans_indices)
                    
        if used_indices:
            ans = sum( line.count('#') for line in image ) - len(used_indices)
            return ans 


def build_image(grid, mat_map, int_to_state_to_conf):
    nn, mm = len(grid), len(grid[0])
    mat_sz = len(mat_map[grid[0][0][0]][0])
    
    image = []
    new_map = {}
    for row in grid:
        for rc in row:
            ind, state_ = rc
            state = convert_to_tuple(state_)
            rot, h_flip, v_flip = int_to_state_to_conf[ind][state]
            matt = rotate_mat(mat_map[ind], rot)
            matt = flip_mat_horizontal(matt) if h_flip else matt
            matt = flip_mat_vertical(matt) if v_flip else matt
            new_map[ind] = matt
            
        row_img = []
        for ii in range(1, mat_sz-1): 
            row_img.append( ''.join(new_map[rc[0]][ii][1:-1] for rc in row) )

        image.extend( row_img )
    return image
    


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)






# debug functions ---------------------------------
def print_matrix(matrix):
    for row in matrix:
        print(row)

def print_matrix_sides(sides):
    print(sides['top'])
    width = len(sides['top']) 
    for lchar, rchar in zip(sides['left'][1:-1], sides['right'][1:-1]):
        print(lchar + ' '* (width-2) + rchar)
    print(sides['bot'])
    return None



def print_grid_alloc(grid):
    return None
    print("GRID ------")
    for row in grid:
        for ee in row:
            print(ee[0], end = ' ')
        print()
    print(" ------")


    
if __name__ == '__main__':
    main()
