import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
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
    I have an equation of the form Ax=b where all x is vector of size k*1, b is vector of size d*1 and A is a matrix of d*k, all are integer values.
    Values in A, b, x are non-negative integers.
    I need to solve for x (A and b are known) that minimise L1 norm of x.

What are some possible solutions?
"""
def solve_min_l1_integer(A, b):
    """
    Solves Ax = b for a vector x of non-negative integers such that 
    the L1 norm (sum of x) is minimized.

    Parameters:
    -----------
    A : array-like, shape (d, k)
        The coefficient matrix (integers).
    b : array-like, shape (d,)
        The target vector (integers).

    Returns:
    --------
    x : numpy.ndarray or None
        The optimal integer vector x of shape (k,) if a solution exists.
        Returns None if no feasible solution is found.
    """
    # Ensure inputs are numpy arrays
    A_arr = np.atleast_2d(A)
    b_arr = np.atleast_1d(b)
    
    d, k = A_arr.shape
    
    # 1. Define Objective Function
    # We want to minimize L1 norm. Since x >= 0, L1 norm is simply sum(x).
    # This is equivalent to minimizing c @ x where c is a vector of ones.
    c = np.ones(k)
    
    # 2. Define Constraints (Ax = b)
    # LinearConstraint requires lb <= A @ x <= ub.
    # For equality Ax = b, we set both lb and ub to b.
    constraints = LinearConstraint(A_arr, lb=b_arr, ub=b_arr)
    
    # 3. Define Integrality
    # A vector of 1s means every variable x_i must be an integer.
    integrality = np.ones(k)
    
    # 4. Define Bounds
    # x >= 0 for all x
    bounds = Bounds(lb=0, ub=np.inf)
    
    # 5. Solve using Mixed-Integer Linear Programming
    res = milp(c=c, constraints=constraints, integrality=integrality, bounds=bounds)
    
    # 6. Process Result
    if res.success:
        # The solver returns floats; round them to nearest integers
        return np.round(res.x).astype(int)
    else:
        return None


@aoc_comm(settings, level=2)
def solve_l2(input_str):  # input data will be passed to this as string
    inp = parse_input(input_str)

    def solve(dest_node, ops):
        b = np.array(dest_node)
        k, d = len(ops), len(dest_node)
        A = np.zeros((d, k), dtype=int)
        for col_ind, light_inds in enumerate(ops):
            for row_ind in light_inds:
                A[row_ind, col_ind] = 1

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
