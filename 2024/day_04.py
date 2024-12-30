from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    'day' : 4,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''

EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    return inp_content
    

def to_mat(inp, pad_ln):
    mat = []
    for line in inp:
        mat.append(list('.'*(pad_ln-1) + line + '.'*(pad_ln-1)))
    
    pad = list('.'*(len(mat[0])))
    mat = [pad]*(pad_ln-1) + mat + [pad]*(pad_ln-1)
    return mat


DIAGS = [
    [(-1, -1), (1, 1)], # diags 1
    [(-1, 1), (1, -1)], # diags 2
]

INCS = [
    (0, 1), (0, -1), # horizontal
    (1, 0), (-1, 0), # vertical
] + DIAGS[0] + DIAGS[1]


    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    WORD = 'XMAS'
    LN = len(WORD)

    inp = parse_input(input_str)
    mat = to_mat(inp, LN)

    def get_count1(mat, ii, jj, word):
        wl = len(word)
        ct = 0
        for step_i, step_j in INCS:
            ss = ''.join([mat[ii+sn*step_i][jj+sn*step_j] for sn in range(wl)])
            if ss == word:
                ct += 1
        return ct
    
    ans = 0
    for ii in range(LN-1, len(mat)-LN+1):
        for jj in range(LN-1, len(mat[ii])-LN+1):
            ans += get_count1(mat, ii, jj, WORD)

    return ans



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    WORD = 'MAS'
    LN = len(WORD)

    inp = parse_input(input_str)
    mat = to_mat(inp, LN)

    def get_count2(mat, ii, jj, diag_ins, word):
        wl = len(word)
        offset = wl // 2
        matches = 0
        for step_i, step_j in diag_ins:
            ss = ''.join([mat[ii+sn*step_i - step_i*offset][jj+sn*step_j - step_j*offset] for sn in range(wl)])
            if ss == word:
                matches += 1
        return matches

    ans = 0
    for ii in range(LN-1, len(mat)-LN+1):
        for jj in range(LN-1, len(mat[ii])-LN+1):
            if get_count2(mat, ii, jj, DIAGS[0], WORD) > 0 and get_count2(mat, ii, jj, DIAGS[1], WORD) > 0:
                ans += 1

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
