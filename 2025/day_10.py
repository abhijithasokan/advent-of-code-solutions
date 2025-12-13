from functools import lru_cache
import pulp
import numpy as np
from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    "day": 10,
    "year": 2025,
    "cookie-path": os.path.realpath("../aoc_cookie.json"),
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split("\n")
    for line in inp_content:
        sp1, sp2 = line.find("]"), line.find("{")
        lights = line[1:sp1].strip()
        switches_rr = line[sp1 + 1 : sp2].strip().split(" ")
        switches = []
        for sr in switches_rr:
            switches.append(tuple(map(int, sr.strip("()").split(","))))
        costs = tuple(map(int, line[sp2 + 1 : -1].strip("{}").split(",")))

        yield lights, switches, costs


from heapq import heappop, heappush
from functools import lru_cache


def solve(dest_node, edge_ops, costs):
    qq = []
    heappush(qq, (0, 0, None))  # cost, node
    visited = set()

    while qq:
        dist, node, last_edge_op = heappop(qq)
        if node == dest_node:
            return dist
        if node in visited:
            continue

        visited.add(node)
        for edge_op, cost in zip(edge_ops, costs):
            if edge_op == last_edge_op:
                continue
            next_node = node ^ edge_op
            heappush(qq, (dist + cost, next_node, edge_op))

    raise ValueError("Node not found")


@aoc_comm(settings, level=1)
def solve_l1(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)

    def active_bit_list_to_num(bit_list):
        num = 0
        for bit_ind in bit_list:
            num |= 1 << bit_ind
        return num

    ans = 0
    for lights, switches, costs in inp:
        dest_node = int(lights.replace(".", "0").replace("#", "1")[::-1], 2)
        edge_ops = [active_bit_list_to_num(switch) for switch in switches]
        edge_costs = [1] * len(edge_ops)

        ans += solve(dest_node, edge_ops, edge_costs)

    return ans


"""
The below function is generated with Gemini AI assistance (only this linear solver function).
Prompt used:
    I have an equation of the form x^TA=b where x is vector of size k, b is vector of size d and A is a matrix of (k*d).
    Values in A, b, x are non-negative integers.
    I need to solve for x (A and b are known) that minimise L1 norm of x.

What are some possible solutions?
"""
def solve_min_l1_integer(A, b):
    """
    Solves x^T A = b for x >= 0 (integers) minimizing sum(x).
    Args:
        A: Matrix (k x d)
        b: Vector (size d)
    Returns:
        x: Solution vector (size k) or None if infeasible
    """
    k, d = A.shape

    # 1. Initialize the Model (Minimize)
    prob = pulp.LpProblem("Minimize_L1_NonNeg_Integer", pulp.LpMinimize)

    # 2. Define Variables
    # lowBound=0 allows zero. cat='Integer' enforces 0, 1, 2...
    x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in range(k)]

    # 3. Objective: Minimize sum of x
    prob += pulp.lpSum(x_vars)

    # 4. Constraints: x.T * A = b  (Equivalent to A.T * x = b.T)
    # We iterate through columns of A (which map to elements of b)
    for j in range(d):
        # Sum(x_i * A[i][j]) == b[j]
        dot_product = pulp.lpSum([x_vars[i] * A[i][j] for i in range(k)])
        prob += dot_product == b[j]

    # 5. Solve
    # PULP_CBC_CMD is the default solver, msg=0 suppresses log output
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    # 6. Check Result
    if pulp.LpStatus[prob.status] == "Optimal":
        return np.array([int(pulp.value(v)) for v in x_vars])
    else:
        return None


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)

    def solve(dest_node, ops):
        b = np.array(dest_node)
        k, d = len(ops), len(dest_node)
        A = np.zeros((k, d), dtype=int)
        for i in range(k):
            for ind in ops[i]:
                A[i][ind] = 1

        res = solve_min_l1_integer(A, b)
        if res is None:
            raise ValueError("Node not found")
        return sum(res)

    ans = 0
    for _, edge_ops, dest_node in inp:
        ans += solve(dest_node, edge_ops)
    return ans


def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == "__main__":
    main()
