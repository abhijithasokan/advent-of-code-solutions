from utils import aoc_comm, run_example
import os

from collections import defaultdict
import itertools

# --- update day/ year for each challenge
settings = {
    'day' : 5,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13
102|100
100|101
101|75

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n\n')

    rules = [tuple(map(int, ss.split('|'))) for ss in inp_content[0].split('\n')]
    ordering = [list(map(int, line.split(','))) for line in inp_content[1].split('\n')]

    return rules, ordering


'''
    How does ordering check work with just checking the child and not all descendents?
    - We only consider the sub graph with nodes given in the ordering list. 
    - Proof 
        - let n_1,....n_k...n_z be topological ordering according to the graph
        - let - pos(n) be the position in the ordering
        - Our algorithm makes sure that pos(n_{i}) < pos(n_{i+1}) for all `i`
            - This by induction also ensures that pos(n_{k}) < pos(n_{m}) for all k < m
'''
def is_valid_ordering(adj_list, order):
    def is_child(node, parent):
        return node in adj_list[parent]
    
    for ind in range(1, len(order)):
        cur_node = order[ind]
        if any(is_child(cur_node, order[ii]) for ii in range(ind)):
            return False
        
    return True
    

@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    rules, ordering = parse_input(input_str)

    adj_list = defaultdict(list)
    for n1, n2 in rules:
        adj_list[n2].append(n1)

    ans = 0
    for order in ordering:
        n = len(order)
        if n%2 == 0:
            raise ValueError("Expects even length for ordering")

        if is_valid_ordering(adj_list, order):
            ans += order[n//2]

    return ans



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    rules, ordering = parse_input(input_str)

    adj_list = defaultdict(list)
    for n1, n2 in rules:
        adj_list[n2].append(n1)


    def get_sort_key(active_nodes):
        active_nodes = set(active_nodes)
        cur_adj_list = {
            node : list(filter(lambda x: x  in active_nodes, adjs)) 
                for node, adjs in adj_list.items() if node in active_nodes
        }

        non_start_nodes = set(ee for ee in itertools.chain(*cur_adj_list.values()))
        start_nodes = active_nodes - non_start_nodes

        topo_ordering = []
        visited = set()
        def dfs(node, visited):
            if node in visited:
                return 
            
            visited.add(node)
            for next_node in cur_adj_list[node]:
                dfs(next_node, visited)
            topo_ordering.append(node)

        for start_node in start_nodes:
            dfs(start_node, visited)

        N = len(topo_ordering)
        node_to_topo_order = defaultdict(lambda : N)
        node_to_topo_order.update((node,ind) for ind, node in enumerate(topo_ordering))
        key = lambda x: node_to_topo_order[x]
        return key


    ans = 0
    for order in ordering:
        n = len(order)
        if n%2 == 0:
            raise ValueError("Expects even length for ordering")

        if not is_valid_ordering(adj_list, order):
            order.sort(key=get_sort_key(order))
            ans += order[n//2]

    return ans




def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP_1))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP_2))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
