from utils import aoc_comm
import os
import typing
import itertools

settings = {
    'day' : 19,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def build_rev_transform_map(transforms):
    def build_rev_transform(params):
        ll = [None, None, None]
        for ind, xx in enumerate(params):
            cord, dirr = xx
            ll[cord] = (ind, dirr)
        return tuple(ll)

    param_to_ind = { param: ind for ind, param in enumerate(transforms)}
    rev_trans_map = { ind: param_to_ind[build_rev_transform(param)] for ind, param in enumerate(transforms)}
    return rev_trans_map


TRANSFORMS = [((0, 1), (1, 1), (2, 1)), ((2, -1), (1, 1), (0, 1)), ((0, -1), (1, 1), (2, -1)), ((2, 1), (1, 1), (0, -1)), ((0, 1), (2, 1), (1, -1)), ((1, 1), (2, 1), (0, 1)), ((0, -1), (2, 1), (1, 1)), ((1, -1), (2, 1), (0, -1)), ((0, 1), (1, -1), (2, -1)), ((2, 1), (1, -1), (0, 1)), ((0, -1), (1, -1), (2, 1)), ((2, -1), (1, -1), (0, -1)), ((0, 1), (2, -1), (1, 1)), ((1, -1), (2, -1), (0, 1)), ((0, -1), (2, -1), (1, -1)), ((1, 1), (2, -1), (0, -1)), ((2, -1), (0, -1), (1, 1)), ((1, -1), (0, -1), (2, -1)), ((2, 1), (0, -1), (1, -1)), ((1, 1), (0, -1), (2, 1)), ((2, 1), (0, 1), (1, 1)), ((1, -1), (0, 1), (2, 1)), ((2, -1), (0, 1), (1, -1)), ((1, 1), (0, 1), (2, -1))]
TRANS_ID_MAP = build_rev_transform_map(TRANSFORMS)
NUM_COMMON_PTS = 12


class Point:
    def __init__(self, coord):
        self.coord_ = tuple(coord)
        assert len(self.coord_) == 3

    def __add__(self, other):
        return Point((p1+p2 for p1, p2 in zip(self.coord_, other.coord_)))

    def __sub__(self, other):
        return Point((p1-p2 for p1, p2 in zip(self.coord_, other.coord_)))

    def __hash__(self):
        return hash(self.coord_)

    def __eq__(self, other):
        return self.coord_ == other.coord_

    def transform(self, trans_id):
        params = TRANSFORMS[trans_id]
        t = self.coord_
        return Point((t[params[ind][0]]*params[ind][1] for ind in range(len(t))))

    def get_manhattan_dist(self, other):
        return sum(abs(p1-p2) for p1, p2 in zip(self.coord_, other.coord_))


class SensorData:
    def __init__(self, lst):
        self.coords_ = lst
        self.diffs_ = self.build_diffs(self.coords_)

    @classmethod
    def build_from_list(cls, lst):
        coords = list(map(lambda cord: Point(cord), lst))
        return SensorData(coords)

    @staticmethod
    def build_diffs(coords):
        all_diffs = []
        for ii in range(len(coords)):
            diffs = set(coords[jj] - coords[ii] for jj in range(len(coords)) if jj != ii)
            all_diffs.append((ii, diffs))
        return all_diffs

    def get_transformed_coords(self, trans_id):
        coords = [pt.transform(trans_id) for pt in self.coords_]
        return coords

    def populate_oriented_data(self):
        global TRANSFORMS
        ord_data = []

        for trans_id in range(len(TRANSFORMS)):
            coords = self.get_transformed_coords(trans_id)
            diffs = self.build_diffs(coords)
            ord_data.append( (trans_id, (coords, diffs)) )
        self.ord_data_ = ord_data

    def try_fix(self, other):
        for trans_id, items in self.ord_data_:
            coords, diffs = items
            for pt_id, diff in diffs:
                for other_id, other_diff in other.diffs_:
                    common_diff = diff & other_diff
                    if len(common_diff) >= (NUM_COMMON_PTS - 1):
                        other_pt = other.coords_[other_id].transform(TRANS_ID_MAP[trans_id])
                        offset = self.coords_[pt_id] - other_pt
                        return TRANS_ID_MAP[trans_id], offset

    def fixate(self, trans_id, offset):
        self.coords_ = [cord + offset for cord in self.get_transformed_coords(trans_id)]
        self.offset_ = offset
        self.populate_oriented_data()
        del self.diffs_


def parse_input(inp_content):
    inp_content = inp_content.strip()
    data = []
    for ee in inp_content.split('\n\n'):
        lines = ee.split('\n')
        coords = []
        for line in lines[1:]:
            coord = tuple(map(int, line.split(',')))
            coords.append(coord)
        data.append(SensorData.build_from_list(coords))
    return data


def fix(sds: typing.List[SensorData]):
    sds[0].fixate(0, Point((0,0,0)))
    fixed_sensors = [sds[0]]
    unprocessed = set(range(1, len(sds)))
    while unprocessed:
        for ind in unprocessed:
            is_fixed = False
            for ind2, f_sd in enumerate(fixed_sensors):
                res = f_sd.try_fix(sds[ind])
                if res is None:
                    continue
                trans_id, offset = res
                sds[ind].fixate(trans_id, offset)
                fixed_sensors.append(sds[ind])
                unprocessed.discard(ind)
                is_fixed = True
                break
            if is_fixed:
                break
        else:
            assert 0, "Nothing fixed"

    return fixed_sensors


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    fixed_inp = fix(parse_input(input_str))
    coords = set()
    for sd in fixed_inp:
        coords.update(sd.coords_)
    return len(coords)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    fixed_inp = fix(parse_input(input_str))
    locs = [sd.offset_ for sd in fixed_inp]
    ans = max(map(lambda cc: cc[0].get_manhattan_dist(cc[1]),  itertools.product(locs, repeat=2)))
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
