from utils import aoc_comm
import os
import re
from collections import Counter, defaultdict
import math
import functools
import itertools

# --- update day/ year for each challenge
settings = {
    'day' : 24,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


# This is incomplete version of the code --------
# Lot of manual decoding was done on the ALU parsed code ------


example_inp=''''''


def parse_input(inp_content):
    inp_content = inp_content.strip()
    for ee in inp_content.split('\n'):
        yield ee.strip()

# class ShrodingerVar:
#     VAR_NUM = 1
#     def __init__(self, eqn):
#         self.eqn = eqn
#         self.id_ = ShrodingerVar.VAR_NUM
#         ShrodingerVar.VAR_NUM += 1
#
#     def __hash__(self):
#         return hash(self.inp_num, self.const)
#
#     def __str__(self):
#         return 'Sch_%d'%(self.id_)


class LinearEqn:
    def __init__(self):
        self.vars = defaultdict(int)
        self.const = 0

    def __add__(self, other):
        for var_name, coeff in other.vars.items():
            self.vars[var_name] += coeff
        self.const += other.const

    def __mult__(self, other):
        pass


class Operand:
    INP_COUNT = 0
    OP_MAP = {
        '+': lambda x, y: x + y,
        '*': lambda x, y: x * y,
        '=': lambda x, y: x == y,
        '~': lambda x, y: x != y,
        '%': lambda x, y: x % y,
    }
    def __init__(self):
        self.operations = []
        self.operands = []
        self.val = 0
        self.min_val = 0
        self.max_val = 0

    def get_expr(self):
        exp = str(self.val)
        assert len(self.operands) == len(self.operations), '|'.join(self.operations) + ' ' + ','.join(self.operands)
        for ind, op in enumerate(self.operations):
            if op == 'mul':
                exp = '(%s) * %s'%(exp, self.operands[ind])
            elif op == 'mod':
                exp = '(%s)'%exp + " % " + self.operands[ind]
            elif op in ['=', '~']:
                exp = '(%s) %s (%s)'%(exp, op, self.operands[ind])
            elif op == 'div':
                exp = '(%s) / %s' % (exp, self.operands[ind])
            elif op == 'add':
                exp = '%s + %s' % (exp, self.operands[ind])
        return exp


    def remove_unwanted_paren(self, exp):
        pass

    def tokenize(self, exp: str):
        tokens = []
        number = None
        for ch in exp:
            if ch in ['(', ')', '+', '-', '/', '%', '=', '~']:
                tokens.append(ee)

            if ch.isdigit():
                if number is None:
                    number = int(ch)
                else:
                    number = number*10 + int(ch)
            elif number is not None:
                tokens.append(number)
                number = None

        return tokens

    def reduce_expr(self, exp):
        tokens = self.tokenize(exp)
        new_expr = []
        operators = []
        operands = []

        for pos, ch in enumerate(exp):
            if ch == '(':
                operators.append(len(operands))
            elif ch == ')':
                while operators[-1] != '(':
                    op = operators.pop()
                    if isinstance(operands[-1], int) and isinstance(operands[-2], int):
                        v2 = operands.pop()
                        v1 = operands.pop()
                        res = Operand.OP_MAP[op](v1, v2)
                        operands.append(res)
                    else:
                        pass


    def get_literal(self, operand):
        if isinstance(operand, Operand):
            if operand.val is not None:
                return operand.val
            else:
                return '(' + operand.get_expr() + ')'
        else:
            return int(operand)


    def add_operation(self, op, operand_orig):
        operand = self.get_literal(operand_orig)
        if self.eager_eval(operand):
            return

        #if it reaches here,

        if op == 'add':
            if len(self.operations) == 0:
                self.val = operand
                return
            self.update_range(operand)
        elif op == 'inp':
            print("---------------------")
            self.operations.clear()
            self.operands.clear()
            self.val = 'I[%d]'%Operand.INP_COUNT
            Operand.INP_COUNT += 1
            self.max_val = 9
            self.min_val = 0
            return
        elif op == 'eql':
            op = '='

        self.operations.append(op)
        self.operands.append(operand)
        #self.reduce()
        assert len(self.operands) == len(self.operations) #, "" + op +" "+ operand

    def get_range(self):
        if self.val is not None:
            return self.val ,self.val
        return self.min_val, self.max_val

    def is_unequal(self, operand):
        if isinstance(operand, int):
            if self.val is not None:
                return self.val != operand
            if self.min_val is not None and operand < self.min_val:
                return True
            if self.max_val is not None and operand > self.max_val:
                return True
        elif isinstance(operand, Operand):
            if self.val is not None and operand.val is not None:
                return self.val != operand.val
            if self.min_val is not None and operand.max_val is not None:
                if operand.max_val < self.min_val:
                    return True
            if self.min_val is not None and operand.max_val is not None:
                if operand.max_val < self.min_val:
                    return True
        return None



    def eager_eval(self, op, operand):
        if isinstance(operand, int) and self.val is not None:
            self.val = Operand.OP_MAP[op](self.val, operand)
            return True
        if isinstance(operand, Operand):
            if operand.val is not None and self.val is not None:
                self.val = Operand.OP_MAP[op](self.val, operand.val)
                return True
            if op == 'eql':
                res = self.is_unequal(operand)
                if res is not None:
                    self.val = int(not res)
        self.val = None
        return False




    def update_range(self, operand, op):
        if isinstance(operand, Operand):
            min_v, max_v = operand.get_range()
            min_v = min_v or 0
            max_v = max_v or 0
        else:
            min_v = max_v = int(operand)
        if op == '+':
            self.min_val += min_v
            self.max_val += max_v
        elif op == '%':
            self.min_val = 0
            self.max_val = max_v - 1
        elif op == 'inp':
            self.min_val, self.max_val = 0, 9


    # def reduce(self):
    #     if len(self.operations) < 2:
    #         return
    #     if self.operations[-1] == self.operations[-2] == '=':
    #         if self.operands[-1] == '0':
    #             self.operands.pop()
    #             self.operations.pop()
    #             self.operations[-1] = '~'




def build_func(program):
    operands = {
        'x': Operand(),
        'y': Operand(),
        'z': Operand(),
        'w': Operand(),
    }

    for line in program:
        if not line:
            continue
        items = line.split(' ')

        op = items[0].strip()
        operand1 : Operand = operands[items[1].strip()]
        operand2 = items[2].strip() if len(items) > 2 else ''
        operand2 = operands.get(operand2, operand2)
        operand1.add_operation(op, operand2)

    #print(operands['x'].get_expr())
    #print(operands['y'].get_expr())
    exp = operands['y'].get_expr()
    exp = exp.replace('(((0)) % 26 + 12)', '12')
    print(exp)
    #print(operands['w'].get_expr())
    return None


def get_read_num(number):
    ss = str(number)
    for ee in ss:
        yield int(ee)

def test_prg(func, number):
    if '0' in str(number):
        return False
    gnum = get_read_num(number)
    read_num = lambda: next(gnum)
    x, y, z, w = func(read_num, [0, 0, 0, 0])
    return z == 0


@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    program = parse_input(input_str)
    ret = build_func2(program)
    # num = 99999999999999
    # steps = 10**9
    # while num >= 11111111111111:
    #     if test_prg(func, num):
    #         return num
    #     num -= 1
    #     steps -= 1
    #     if steps == 0:
    #         print(num)
    #         steps = 10**9
    return ret




@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    return None



def main():
    print("[L1] Ex: ", solve_l1.raw_(example_inp))
    l1_status = solve_l1()
    print(l1_status)

    print("[L2] Ex: ", solve_l2.raw_(example_inp))
    l2_status = solve_l2()
    print(l2_status)










#-------------------------------------------------
def build_func2(program):
    translated_program = []
    x, y, z, w = 0, 0, 0, 0

    st_to_op = {
        'add' : '+=',
        'mul' : '*=',
        #'inp' : '= read()',
        'div' : '//=',
        'mod' : '%=',
        #'eql' : '= ()'
    }
    inp_use_count = 0
    for line in program:
        if not line:
            continue
        items = line.split(' ')

        op = items[0].strip()
        operand1 = items[1].strip()
        operand2 = items[2].strip() if len(items) > 2 else ''

        new_line = operand1 + ' '
        if op in ['div', 'mul'] and operand2 == '1':
            continue
        elif op == 'mul' and operand2 == '0':
            new_line = new_line + '= 0'
        elif op in st_to_op:
            new_line = new_line + st_to_op[op] + (' ' + items[2] if len(items) > 2 else '')
        elif op == 'eql':
            new_line = new_line + '= int(%s == %s)'%(operand1, items[2])
        elif op == 'inp':
            new_line = new_line + '= inp[%d]'%(inp_use_count)
            inp_use_count += 1

        #print(op, operand1, new_line)
        translated_program.append(new_line)

    func_line = '''def func(varss, inp):\n\tx,y,z,w = varss\n\t''' + '\n\t'.join(translated_program) + '\n\treturn x, y, z, w'
    gb, lc = {}, {}
    open('func_MAIN.py', 'w').write(func_line)
    exec(func_line, gb, lc)
    #print(gb, lc)
    return lc['func']
#----------------------------------------------------------------------------------


if __name__ == '__main__':
    main()
