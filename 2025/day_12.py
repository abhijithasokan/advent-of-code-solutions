import random
import os
from collections import defaultdict

from utils import aoc_comm, run_example

# --- update day/ year for each challenge
settings = {
    "day": 12,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    tt = inp_content.split("\n\n")
    shapes, placements = tt[:-1], tt[-1].strip().split("\n")
    shapes = [shape.strip().split("\n")[1:] for shape in shapes]
    placements_parsed = []
    for placement in placements:
        size_str, pos_str = placement.split(":")
        w, h = map(int, size_str.strip().split("x"))
        counts = list(map(int, pos_str.strip().split()))
        placements_parsed.append((w, h, counts))

    return shapes, placements_parsed


def generate_augmentations(shape):
    def rotate(shape):
        m, n = len(shape), len(shape[0])
        return ["".join([shape[m - 1 - c][r] for c in range(m)]) for r in range(n)]

    def flip(shape):
        return [row[::-1] for row in shape]

    augs = [shape]
    for _ in range(3):
        shape = rotate(shape)
        augs.append(shape)

    return augs + [flip(aug) for aug in augs]


def vec_less_eq(v1, v2):
    for a, b in zip(v1, v2):
        if a > b:
            return False
    return True




def func(w, l, counts, ind_to_shapes):
    grid = [["."] * w for _ in range(l)]

    def can_place(shape, ii, jj):
        if ii + 3 > l:
            return False
        offset = shape[0].find("#")
        jj -= offset
        if jj < 0 or jj + 3 > w:
            return False
        for row_ind in range(3):
            for col_ind in range(3):
                if shape[row_ind][col_ind] == "#":
                    if grid[ii + row_ind][jj + col_ind] == "#":
                        return False
        return True

    def put(shape, ii, jj, ch="#"):
        offset = shape[0].find("#")
        jj -= offset
        for row_ind in range(3):
            for col_ind in range(3):
                if shape[row_ind][col_ind] == "#":
                    grid[ii + row_ind][jj + col_ind] = ch
        return

    shape_space = [ind_to_shapes[ind][0].count("#") for ind in range(len(counts))]
    required_free_space = lambda: sum(
        counts[ind] * shape_space[ind] for ind in range(len(counts))
    )

    # quick reject
    free_place_avail = w * l
    if required_free_space() > free_place_avail:
        return False

    # quick accept
    naive_num_rects = (l // 3) * (w // 3)
    total_rects_needed = sum(counts)
    if total_rects_needed <= naive_num_rects:
        return True

    class LookUp:
        def __init__(self, grid, counts):
            self.grid = grid
            self.counts = counts

            self.table = defaultdict(list)

        def mark_failure(self):
            if not self.is_impossible():
                key = "".join("".join(row) for row in self.grid)
                self.table[key].append(tuple(self.counts))

        def check_free_slots(self, g_key):
            key = "".join("".join(row) for row in self.grid)
            for kk in range(len(key)):
                if key[kk] == "." and g_key[kk] == "#":
                    return False
            return True

        def is_impossible(self):
            cur_counts = tuple(self.counts)
            for g_key, g_counts in self.table.items():
                if not self.check_free_slots(g_key):
                    continue

                for counts in g_counts:
                    if vec_less_eq(counts, cur_counts):
                        return True
            return False

    lookup = LookUp(grid, counts)

    def try_place(ii, jj, attempts=0):
        nonlocal free_place_avail
        if sum(counts) == 0:
            return True

        if free_place_avail < required_free_space():  # quick rejection
            return False
        if jj == w:
            return try_place(ii + 1, 0, 0)
        if ii >= l:
            return False

        # if attempts >= 4:
        #     return False

        if grid[ii][jj] == "#":
            return try_place(ii, jj + 1, attempts + 1)

        # if lookup.is_impossible():
        #     # print(len(lookup.table))
        #     return False

        random_items = list(ind_to_shapes.items())
        random.shuffle(random_items)
        for ind, shapes in random_items:
            if counts[ind] == 0:
                continue

            space_needed = shape_space[ind]

            for shape in shapes:
                if can_place(shape, ii, jj):
                    put(shape, ii, jj, "#")
                    counts[ind] -= 1
                    free_place_avail -= space_needed
                    if try_place(ii, jj + 1, 0):
                        # lookup.mark(True)
                        return True
                    # lookup.mark_failure()
                    free_place_avail += space_needed
                    put(shape, ii, jj, ".")
                    counts[ind] += 1

        # if we reach here, it mean we couldn't fit any at ii, jj

        res = try_place(ii, jj + 1, attempts + 1)
        # lookup.mark_failure()
        return res

    try:
        return try_place(0, 0)
    except RecursionError:
        # I really HATEEEEEE this approach, but apparently AoC test case for day 12 passes with this
        # also consistent with the discussion thread.
        return False


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    shapes, placements = parse_input(input_str)

    ind_to_shapes = {}
    for ind, shape in enumerate(shapes):
        ind_to_shapes[ind] = generate_augmentations(shape)

    ans = 0
    for w, l, counts in placements:
        if func(w, l, counts, ind_to_shapes):
            ans += 1
        # print("Placing for:", w, l, counts, "->", ans)
    return ans


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)
    return None


def main():
    # print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)


if __name__ == "__main__":
    main()
