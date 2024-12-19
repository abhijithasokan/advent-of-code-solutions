from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    'day' : 15,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def find_pos(grid, ch):
    return ((ii, jj) for ii, line in enumerate(grid) for jj, cc in enumerate(line) if cc == ch)

def parse_input(inp_content):
    grid, moves = inp_content.strip().split('\n\n')
    grid = [list(line) for line in grid.split('\n')]

    moves = moves.split('\n')
    return grid, moves, next(find_pos(grid, '@'))
    
    
STEPS = {
    '<' : (0, -1),
    '>' : (0, 1),
    '^' : (-1, 0),
    'v' : (1, 0),
}

TUP_ADD = lambda x, y: (x[0]+y[0], x[1]+y[1])

def compute_gps(grid, box_ch):
    gps_sm = 0
    for ii, line in enumerate(grid):
        for jj, ch in enumerate(line):
            if ch == box_ch:
                gps = 100 * ii + jj
                gps_sm += gps

    return gps_sm


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    grid, moves, pos = parse_input(input_str)

    def take_step(grid, pos, step):
        offset = STEPS[step]
        new_pos = TUP_ADD(pos, offset)

        if grid[new_pos[0]][new_pos[1]] == '#':
            return pos
        
        elif grid[new_pos[0]][new_pos[1]] == '.':
            grid[new_pos[0]][new_pos[1]] = '@'
            grid[pos[0]][pos[1]] = '.'
            return new_pos
        
        else:
            while grid[new_pos[0]][new_pos[1]] == 'O':
                new_pos = TUP_ADD(new_pos, offset)

            if grid[new_pos[0]][new_pos[1]] == '.':
                grid[new_pos[0]][new_pos[1]] = 'O'
                grid[pos[0]][pos[1]] = '.'
                new_pos = TUP_ADD(pos, offset)
                grid[new_pos[0]][new_pos[1]] = '@'
                return new_pos
        
        return pos


    for move in moves:
        for step in move:
            pos = take_step(grid, pos, step)

    return compute_gps(grid, box_ch='O')



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    grid, moves, _ = parse_input(input_str)
    conv = lambda x: x.replace('O', '[]').replace('#', '##').replace('.', '..').replace('@', '@.')
    grid = [ list(conv(''.join(line))) for line in grid ]
    pos = next(find_pos(grid, '@'))


    cache = {}
    def check(pos, offset, partner_called=False):
        res = cache.get(pos, None)
        if res is not None:
            return res
        
        np = TUP_ADD(pos, offset)
        gch = grid[np[0]][np[1]]

        if gch == '#':
            return False
        elif gch == '.':
            return True
        elif gch in '[]':
            if partner_called:
                return check(np, offset)

            part_offset = (0, -1) if gch == ']' else (0, 1)
            part_pos = TUP_ADD(pos, part_offset)
            res = check(np, offset) and check(part_pos, offset, True)
            cache[pos] = res
            cache[part_pos] = res
            return res
        

    def take_step(grid, pos, step):
        offset = STEPS[step]
        new_pos = TUP_ADD(pos, offset)

        if grid[new_pos[0]][new_pos[1]] == '#':
            return pos
        
        elif grid[new_pos[0]][new_pos[1]] == '.':
            grid[new_pos[0]][new_pos[1]] = '@'
            grid[pos[0]][pos[1]] = '.'
            return new_pos
        
        else:
            if step in ('>', '<'):
                while grid[new_pos[0]][new_pos[1]] in '][':
                    new_pos = TUP_ADD(new_pos, offset)

                if grid[new_pos[0]][new_pos[1]] == '.':
                    pp = pos
                    last_ch = grid[pp[0]][pp[1]]
                    grid[pp[0]][pp[1]] = '.'
                    while pp != new_pos:
                        np = TUP_ADD(pp, offset)
                        ch = grid[np[0]][np[1]] 
                        grid[np[0]][np[1]] = last_ch

                        last_ch = ch
                        pp = np

                    return TUP_ADD(pos, offset)
            
            else:
                offset = STEPS[step]
                cache.clear()
                if check(pos, offset):
                    cache[pos] =  True
                    grid_ch_cache = {}
                    poss = set()
                    for pp in cache.keys():
                        bck_pp = TUP_ADD(pp, offset)
                        grid_ch_cache[bck_pp] = str(grid[bck_pp[0]][bck_pp[1]])
                        poss.add(bck_pp)

                    for pp2 in grid_ch_cache.keys():
                        pp = TUP_ADD(pp2, offset)
                        grid[pp[0]][pp[1]] = grid_ch_cache[pp2]
                        poss.discard(pp)
                    
                    for pp in poss:
                        grid[pp[0]][pp[1]] = '.'
                    
                    grid[pos[0]][pos[1]] = '.'
                    new_pos = TUP_ADD(pos, offset)
                    grid[new_pos[0]][new_pos[1]] = '@'
                    return new_pos
        
        return pos


    for move in moves:
        for step in move:
            pos = take_step(grid, pos, step)

    
    # for line in grid:
    #     print(''.join(line))

    return compute_gps(grid, box_ch='[')



def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
