from utils import aoc_comm
import os
import re

# --- update day/ year for each challenge
settings = {
    'day' : 18,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
from collections import Counter, defaultdict
import math
import functools
import itertools



def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n')
    # add further input processing here..
    for exp in inp_content:
        exp = '(' + exp + ')'
        exp = exp.replace('(', ' ( ',).replace(')', ' ) ')
        tokens = exp.split()
        yield tokens

def solve1(tokens):
    operators = []
    operands = []
    for token in tokens:
        if token == '(':
            operators.append('(')
            continue
        elif token == ')':
            t_opn = []
            t_opr = []
            while operators[-1] != '(':
                t_opr.append( operators.pop() )
                t_opn.append( operands.pop() )

            operators.pop()
            pans = operands.pop()
            for rr, nn in list(zip(t_opr, t_opn))[::-1]:
                if rr == '*':
                    pans = pans * nn
                else:
                    pans = pans + nn
                
            token = pans
            
                
        elif token in ('*', '+'):
            operators.append(token)
            continue

        val = int(token)
        if operators and operators[-1] in ('*', '+'):
            op = operators.pop()
            val1 = operands.pop()
            if op =='*':
                operands.append( val1 * val )
            else:
                operands.append( val1 + val )
        else:
            operands.append(val)

    assert(len(operands) == 1)
    return operands[0]


@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    exps = parse_input(input_str)
    ans = 0
    for exp in exps:
        tans = solve1(exp)
        ans += tans
    return ans



def solve2(tokens):
    operators = []
    operands = []
    for token in tokens:
        if token == '(':
            operators.append('(')
            continue
        elif token == ')':
            t_opn = []
            t_opr = []
            while operators[-1] != '(':
                t_opr.append( operators.pop() )
                t_opn.append( operands.pop() )

            operators.pop()
            pans = operands.pop()
            for rr, nn in list(zip(t_opr, t_opn))[::-1]:
                if rr == '*':
                    pans = pans * nn
                else:
                    pans = pans + nn

            token = pans


        elif token in ('*', '+'):
            if token == '*':
                t_opn = []
                while operators and operators[-1] == '+':
                    t_opn.append(operands.pop())
                    operators.pop()
                operators.append(token)
                if t_opn:
                    t_opn.append(operands.pop())
                    pans = reduce(lambda x,y: x+y, t_opn)
                    token = pans
                else:
                    continue
            else:
                operators.append(token)
                continue

        val = int(token)
        if operators and operators[-1] in '+':
            op = operators.pop()
            val1 = operands.pop()
            if op =='*':
                operands.append( val1 * val )
            else:
                operands.append( val1 + val )
        else:
            operands.append(val)

    assert(len(operands) == 1)
    return operands[0]


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    exps = parse_input(input_str)
    ans = 0
    for exp in exps:
        tans = solve2(exp)
        ans += tans
    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
