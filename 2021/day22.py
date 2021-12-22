from utils import aoc_comm
import os
import re

settings = {
    'day' : 22,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip()
    ll = re.findall("([^ ]+) x=([0-9\-]+)\.\.([0-9\-]+),y=([0-9\-]+)\.\.([0-9\-]+),z=([0-9\-]+)\.\.([0-9\-]+)", inp_content, re.DOTALL)
    for dt in ll:
        op, pts = dt[0], tuple(map(lambda x: int(x), dt[1:]))
        x1, x2, y1, y2, z1, z2 = pts
        yield (1 if op.strip() == 'on' else 0), (x1, x2), (y1, y2), (z1, z2)


class Cube:
    def __init__(self, xr, yr, zr):
        self.x1, self.x2 = xr
        self.y1, self.y2 = yr
        self.z1, self.z2 = zr

    def get_intersect(self, other):
        xr = max(self.x1, other.x1), min(self.x2, other.x2)
        yr = max(self.y1, other.y1), min(self.y2, other.y2)
        zr = max(self.z1, other.z1), min(self.z2, other.z2)
        is_valid = lambda rr: rr[0] <= rr[1]
        if is_valid(xr) and is_valid(yr) and is_valid(zr):
            return Cube(xr, yr, zr)
        return None

    def is_valid(self):
        return not (self.x1 > self.x2 or self.y1 > self.y2 or self.z1 > self.z2)

    @staticmethod
    def get_broken(cb1, cb2):
        yield Cube((cb1.x1, cb2.x1-1), (cb1.y1, cb1.y2), (cb1.z1, cb1.z2))  # 1
        yield Cube((cb2.x2+1, cb1.x2), (cb1.y1, cb1.y2), (cb1.z1, cb1.z2))  # 2
        yield Cube((cb2.x1, cb2.x2), (cb2.y2+1, cb1.y2), (cb1.z1, cb1.z2))  # 3
        yield Cube((cb2.x1, cb2.x2), (cb1.y1, cb2.y1-1), (cb1.z1, cb1.z2))  # 4
        yield Cube((cb2.x1, cb2.x2), (cb2.y1, cb2.y2), (cb2.z2+1, cb1.z2))  # 5
        yield Cube((cb2.x1, cb2.x2), (cb2.y1, cb2.y2), (cb1.z1, cb2.z1-1))  # 6

    def __eq__(self, ot):
        return (self.x1, self.x2, self.y1, self.y2, self.z1, self.z2) == (ot.x1, ot.x2, ot.y1, ot.y2, ot.z1, ot.z2)

    def get_sort_key(self):
        return self.get_size(), self.x1, self.x2, self.y1, self.y2, self.z1, self.z2

    def is_inside(self, other):
        intersect = self.get_intersect(other)
        return (intersect is not None) and (intersect == other)

    @staticmethod
    def get_broken_filt(cb1, cb2):
        for cb in Cube.get_broken(cb1, cb2):
            if cb.is_valid():
                yield cb

    def minus(self, other):
        intersect_cube = self.get_intersect(other)
        if intersect_cube is None:
            return [self]
        if intersect_cube == self:
            return []
        return Cube.get_broken_filt(self, intersect_cube)

    def get_size(self):
        return (self.x2-self.x1+1)*(self.y2-self.y1+1)*(self.z2-self.z1+1)


def remove_full_overlaps(active_cubes):
    active_cubes.sort(key=lambda x: x.get_sort_key(), reverse=True)
    filt_cubes = [active_cubes[0]]
    for ind in range(1, len(active_cubes)):
        if not any(cb.is_inside(active_cubes[ind]) for cb in filt_cubes):
            filt_cubes.append(active_cubes[ind])
    return filt_cubes


def break_cubes(cubes, cb):
    new_cubes = []
    for cube in cubes:
        new_cubes.extend(cube.minus(cb))
    return new_cubes


def count_on(inp, filters = None):
    range_check = lambda pt, xr: pt[0] in xr and pt[1] in xr
    active_cubes = []
    for data in inp:
        is_on, coords = data[0], data[1:]
        if (filters is not None) and (not all(range_check(pt, xr) for pt, xr in zip(coords, filters))):
            continue

        cb = Cube(*coords)
        if not is_on:
            active_cubes = break_cubes(active_cubes, cb)
        else:
            active_cubes.append(cb)

    active_cubes = remove_full_overlaps(active_cubes)

    count = active_cubes[0].get_size()
    for ind in range(1, len(active_cubes)):
        rem = [active_cubes[ind]]
        for ind2 in range(ind):
            rem = break_cubes(rem, active_cubes[ind2])
        count += sum(rm.get_size() for rm in rem)

    return count


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    return count_on(parse_input(input_str), filters=(range(-50, 51), range(-50, 51), range(-50, 51)))


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    return count_on(parse_input(input_str))


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()

