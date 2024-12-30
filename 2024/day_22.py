from utils import aoc_comm, run_example
import os

from collections import deque, defaultdict

# --- update day/ year for each challenge
settings = {
    'day' : 22,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''1
10
100
2024
'''

EXAMPLE_INP_2 = '''1
2
3
2024
'''

def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    return map(int, inp_content)
    
    
MASK = 2**24 - 1
def f(x):
    x = (x ^ (x << 6) ) & MASK
    x = (x ^ (x >> 5)) & MASK
    x = (x ^ (x << 11)) & MASK
    return x


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    nums = parse_input(input_str)
    def f_iter(num, n_iters):
        x = num
        for _ in range(n_iters):
            x = f(x)
        return x
        
    ans = 0 
    for num in nums:
        ans += f_iter(num, 2000)
    return ans


def iterate_n_item_with_overlap(data: list, n):
    cur = deque(data[:n])
    yield tuple(cur)
    for ind in range(n, len(data)):
        cur.popleft()
        cur.append(data[ind])
        yield tuple(cur)


@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    nums = parse_input(input_str)

    def f_iter(num, n_iters):
        x = num
        res = [x % 10]
        for _ in range(n_iters):
            x = f(x)
            res.append(x % 10)

        return res
        
    patterns_to_reward = defaultdict(int)
    for num in nums:
        res = f_iter(num, 2000)
        diffs = [a-b for a, b in zip(res[1:], res[:-1])]
        res = res[1:]

        seen_patterns = set()
        for ind, pattern in enumerate(iterate_n_item_with_overlap(diffs, 4)):
            if pattern in seen_patterns:
                continue
            
            seen_patterns.add(pattern)
            patterns_to_reward[pattern] += res[ind+3]

    return max(patterns_to_reward.values())



def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
