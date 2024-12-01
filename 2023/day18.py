from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 18,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


# -- OTHER LIBs that might help while coding the soultions
import re
def parse_input(inp_content, mode):
    inp_content = inp_content.strip().split('\n')
    for line in inp_content:
        res = re.match('(\w) (\d+) \(#([a-f0-9]+)\)', line)
        if mode == 1:
            yield res.group(1), int(res.group(2))
        else:
            yield 'RDLU'[int(res.group(3)[-1])], int(res.group(3)[:-1], base=16)
    

X, Y = 1, 0




def build_polygon(inp):
    polygon = []
    last_pos = (0, 0)

    min_i, max_i = 0, 0
    min_j, max_j = 0, 0
    for move, dist in inp:
        #print(move, dist, color)

        match move:
            case 'U':
                next_pos = last_pos[0] - dist, last_pos[1]
            case 'D':
                next_pos = last_pos[0] + dist, last_pos[1]
            case 'L':
                next_pos = last_pos[0], last_pos[1] - dist
            case 'R':
                next_pos = last_pos[0], last_pos[1] + dist

        min_i, max_i = min(min_i, next_pos[0]), max(max_i, next_pos[0])
        min_j, max_j = min(min_j, next_pos[1]), max(max_j, next_pos[1])

        polygon.append((last_pos, next_pos))
        last_pos = next_pos

    fix_offset = lambda nn: (nn[0] - min_i, nn[1] - min_j)

    polygon = [(fix_offset(n1), fix_offset(n2)) for n1, n2 in polygon]

    return polygon



def compute_area2(polygon):
    verts = [polygon[0][0]]
    for _, n2 in polygon:
        verts.append(n2)

    verts.append(verts[-1])    
    ans = 0
    for v1, v2 in zip(verts[:-1], verts[1:]): # Shoelace algorithm 
        ans += v1[X]*v2[Y] - v2[X]*v1[Y] 
        ans += abs(v1[X] - v2[X]) + abs(v1[Y] - v2[Y]) # additionally for the border
    
    return ans//2 + 1



@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str, 1)
    polygon = build_polygon(inp)
    ans = compute_area2(polygon)
    return ans
    

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str, 2)
    polygon = build_polygon(inp)
    ans = compute_area2(polygon)
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
