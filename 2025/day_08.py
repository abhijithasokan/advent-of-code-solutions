from functools import reduce
import operator
from tkinter import NO, Y
import numpy as np
import scipy
from utils import aoc_comm, run_example
import os


# --- update day/ year for each challenge
settings = {
    "day": 8,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    for line in inp_content:
        yield list(map(int, line.split(",")))


class QuickUnion:
    def __init__(self, ngroups: int):
        self.parent = list(range(ngroups))
        self.sizes = [1] * ngroups
        self._num_active_groups = ngroups

    def root(self, node):
        # standard find with halving path compression
        while node != self.parent[node]:
            self.parent[node] = self.parent[self.parent[node]]
            node = self.parent[node]
        return node

    def is_connected(self, node1, node2):
        return self.root(node1) == self.root(node2)

    def union(self, node1, node2):
        r1 = self.root(node1)
        r2 = self.root(node2)
        if r1 == r2:
            return

        if self.sizes[r1] < self.sizes[r2]:
            r1, r2 = r2, r1

        self.sizes[r1] += self.sizes[r2]
        self.parent[r2] = r1
        self._num_active_groups -= 1
        return

    def get_group_size(self):
        group_sizes = []
        for node, parent in enumerate(self.parent):
            if node == parent:
                group_sizes.append(self.sizes[parent])

        return group_sizes

    @property
    def num_active_groups(self):
        return self._num_active_groups


def compute_increasing_distance_pairs(points):
    nn = len(points)
    points = np.array(points)
    dists = scipy.spatial.distance.pdist(points)  # shape (nn * (nn-1) / 2, )
    sorted_inds = np.argsort(dists)
    X, Y = np.triu_indices(nn, k=1)  # get upper triangular indices without diagonal
    pairs = [(X[inds], Y[inds]) for inds in sorted_inds]
    return pairs


@aoc_comm(settings, level=1)
def solve_l1(input_str, lim: int):  # input data will be passed to this as string
    points = list(parse_input(input_str))
    inc_dist_pairs = compute_increasing_distance_pairs(points)
    qu = QuickUnion(len(points))
    for p1, p2 in inc_dist_pairs[:lim]:
        if not qu.is_connected(p1, p2):
            qu.union(p1, p2)

    group_sizes = qu.get_group_size()
    top_sizes = sorted(group_sizes, reverse=True)[:3]
    ans = reduce(operator.mul, top_sizes)
    return ans


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    points = list(parse_input(input_str))
    inc_dist_pairs = compute_increasing_distance_pairs(points)
    qu = QuickUnion(len(points))

    for p1, p2 in inc_dist_pairs:
        if not qu.is_connected(p1, p2):
            qu.union(p1, p2)
            if qu.num_active_groups == 1:
                return points[p1][0] * points[p2][0]

    return None


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1, 10))
    l1_status = solve_l1(lim=1000)
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
