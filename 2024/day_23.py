from utils import aoc_comm, run_example
import os

from collections import defaultdict

# --- update day/ year for each challenge
settings = {
    'day' : 23,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1


def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    return list(set(tuple(sorted(line.split('-'))) for line in inp_content))
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    edges = parse_input(input_str)

    adj_list = defaultdict(set)
    for n1, n2 in edges:
        adj_list[n1].add(n2)

    print("Num nodes: ", len(adj_list))

    all_cliques_3 = set()
    for n1, n2 in edges:
        clique_3 = set(tuple(sorted([n1, n2, n3])) for n3 in (adj_list[n1] & adj_list[n2]))
        all_cliques_3.update( clique_3 )

    ans = sum(1 if any(node[0]=='t' for node in cq3) else 0 for cq3 in all_cliques_3)
    return ans





def bron_kerbosch(R: set, P: set, X: set, maximal_cliques: list, adj_list):
    '''
        https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    '''
    if len(P) == len(X) == 0:
        maximal_cliques.append(R)
        return 
    
    for v in P.copy():
        bron_kerbosch(R | {v}, P & adj_list[v], X & adj_list[v], maximal_cliques, adj_list)
        P.discard(v)
        X.add(v)

    return 



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    edges = parse_input(input_str)

    adj_list = defaultdict(set)
    for n1, n2 in edges:
        adj_list[n1].add(n2)
        adj_list[n2].add(n1)

    print("Num nodes: ", len(adj_list))

    R = set()
    P = set(adj_list.keys())
    X = set()

    maximal_cliques = []
    bron_kerbosch(R, P, X, maximal_cliques, adj_list)
    max_clique = max(maximal_cliques, key=lambda x: len(x))
    ans = ','.join(sorted(max_clique))
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
