from utils import aoc_comm
import os
import re
from collections import Counter, defaultdict
import math
# --- update day/ year for each challenge
settings = {
    'day' : 13,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


from functools import reduce
import operator

def gcd_extended(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x, y = gcd_extended(b, a%b)
    return gcd, y, x - (a//b)*y


def mod_inverse(b, p):
    gcd, x, y = gcd_extended(b, p)
    if gcd != 1:
        print("Multiplicate inverse doesn't exists")
        return None
    return ( x%p + p ) % p


def min_num_giving_reminders(nums, rems):
    pdt = reduce(operator.mul, nums)
    result = 0
    for num, rem in zip(nums, rems):
        partital_pdt = pdt // num
        result += ( rem * partital_pdt * mod_inverse(partital_pdt, num)  )

    min_num = result % pdt
    return min_num


def parse_input(inp_content):
    inp_content = inp_content.strip().split()
    return int(inp_content[0]), list(map(lambda x: int(x) if x.isnumeric() else -1, inp_content[1].split(',')))

@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    time, buss = parse_input(input_str)
    #print(time, buss)
    ll = []
    for ee in buss:
        if ee == -1:
            continue
        nxt = int(math.ceil(time/ee) * ee)
        ll.append( (nxt, ee) )
        #print (nxt, ee)
    mx = min(ll)
    
    ans = (mx[0] - time)*mx[1]
    
    return ans 


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    _, buss = parse_input(input_str)
    #print(inp)
    nums = []
    rems = []
    for ind, ee in enumerate(buss):
        if ee == -1:
            continue
        nums.append(ee)
        rems.append(ee-ind)

    #print(nums, rems)
    ans = min_num_giving_reminders(nums, rems)
    return ans



def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()




