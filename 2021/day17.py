from utils import aoc_comm
import os
import re
import math
import itertools
import operator

settings = {
    'day' : 17,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    groups = re.search("target area: x=([0-9\-]+)\.\.([0-9\-]+), y=([0-9\-]+)\.\.([0-9\-]+)", inp_content)
    return tuple(int(groups.group(ind)) for ind in range(1, 5))


def tri_num(k):
    return k*(k+1)//2


def find_tri_num_root(tri_num, is_lower_bound = True):
    if not is_lower_bound:
        tri_num += 1
    tri_root = math.sqrt((8*tri_num+1)/4) - 0.5
    return math.ceil(tri_root) - (0 if is_lower_bound else 1)


def get_range(x, y):
    return range(min(x, y), max(x, y)+1)


def vel_bounds(c1, c2, time):
    vc_max = (c2 + tri_num(time-1)) // time
    vc_min = math.ceil((c1 + tri_num(time-1)) / time)
    return get_range(vc_min, vc_max)


def get_velocities(x1, x2, y1, y2):
    time = 0
    velocities = set()
    dist_covered_with_acc = lambda vel, time: vel * time - tri_num(time-1)
    time_limit = max(abs(x2), abs(x1)) or max(abs(x2), abs(x1))

    for time in range(1, time_limit + 1):
        vy_bounds = vel_bounds(y1, y2, time)
        y_velocities = filter(lambda v: dist_covered_with_acc(v, time) in get_range(y1, y2), vy_bounds)

        vx_bounds = vel_bounds(x1, x2, time)
        vx_slow_bound = get_range(find_tri_num_root(x1), find_tri_num_root(x2, False))

        fast_vs = filter(lambda v: (dist_covered_with_acc(v, time) in get_range(x1, x2)) and (v >= time), vx_bounds)
        slow_vs = filter(lambda v: (tri_num(v) in get_range(x1, x2)) and (v <= time), vx_slow_bound)
        x_velocities = itertools.chain(fast_vs, slow_vs)

        velocities.update(itertools.product(x_velocities, y_velocities))
    return velocities


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    x1, x2, y1, y2 = parse_input(input_str)
    velocities = get_velocities(x1, x2, y1, y2)
    vy_max = max(map(operator.itemgetter(1), velocities))
    max_height = tri_num(vy_max)
    return max_height


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    x1, x2, y1, y2 = parse_input(input_str)
    return len(get_velocities(x1, x2, y1, y2))


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
