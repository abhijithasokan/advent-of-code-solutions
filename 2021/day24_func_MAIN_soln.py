def f1(z, w, add_1, add_2, div_n=1):
    x = (z % 26)

    if div_n != 1:     
       z //= div_n

    if x == w - add_1:
        return z
    
    z *= 26
    z += (w+add_2)

    return z


def srange(st, end):
    return set(range(st, end+1))

INP_RANGE = range(1, 10)

# OBSERVATIONS
#   add_2 is always > 0

def get_possible_conf(z, add_1, add_2, div_n):
    confs = []
    if z == 0:
        if div_n != 1:
            for z_can in range(0, 26):
                w_can = z_can + add_1
                if w_can in INP_RANGE:
                    confs.append({'z' : z_can, 'w' : w_can })
        else:
            z_can = 0
            w_can = add_1
            confs.append({'z' : z_can, 'w' : w_can })
    else:
        rem = z % 26
        if (w + add_2) == (z % 26):
            z_can //= 26
            z_can //= div_n
            confs.append({
                'z' : z_can,

            })
    





# def func(inp):
#     args = [
#         (12, 6, 1),
#         (10, 6, 1),
#         (13, 3, 1),
#         (-11, 11, 26),
#         (13, 9, 1),
#         (-1, 3, 26),
#         (10, 13, 1),
#         (11, 6, 1),
#         (0, 14, 26),
#         (10, 10, 1),
#         (-5, 12, 26),
#         (-16, 10, 26),
#         (-7, 11, 26),
#         (-11, 15, 26)
#     ]

#     z = 0
    
#     for i, w_i in enumerate(inp):
#         z = f1(z, w_i, *args[i])
    
#     return z



args = [
    (12, 6, 1),
    (10, 6, 1),
    (13, 3, 1),
    (-11, 11, 26),
    (13, 9, 1),
    (-1, 3, 26),
    (10, 13, 1),
    (11, 6, 1),
    (0, 14, 26),
    (10, 10, 1),
    (-5, 12, 26),
    (-16, 10, 26),
    (-7, 11, 26),
    (-11, 15, 26)
]

z = 0

# for i, w_i in enumerate(inp):
#     z = f1(z, w_i, *args[i])



#import itertools



# RNG = lambda : range(9, 0, -1)
# ct = 0
# SZ = 100000

# cache_table = {}



from functools import lru_cache

cur_path = []


@lru_cache(maxsize=None)
def dfs(z, level):  
    if level == 14:
        if z == 0:
            print(''.join(map(str, cur_path)))
            return True
        else:
            return False
    
    for w in (range(1, 10)):
        cur_path.append(w)
        new_z = f1(z, w, *args[level])
        if dfs(new_z, level+1):
            return True
        cur_path.pop()
    
    return False



dfs(0, 0)