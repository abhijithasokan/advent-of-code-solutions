from utils import aoc_comm, run_example
import os

# --- update day/ year for each challenge
settings = {
    'day' : 9,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP_1 = '''2333133121414131402'''
EXAMPLE_INP_2 = EXAMPLE_INP_1

def parse_input(inp_content):
    inp = list(map(int, inp_content.strip()))
    inp.append(0)
    return list(map(list, zip(inp[::2], inp[1::2])))

def sum_first_n(n):
    if n > 0:
        return (n * (n + 1)) // 2
    return 0
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    ans = 0
    end_pt = len(inp) - 1
    counter = 0
    for ind, item in enumerate(inp):
        ln, space = item
        if ind > end_pt:
            break

        if ln == 0:
            continue

        ans += ind * (counter *ln + sum_first_n(ln-1))
        counter += ln
       
        while space and (end_pt > ind):
            if inp[end_pt][0] != 0:
                space -= 1
                inp[end_pt][0] -= 1
                ans += counter * end_pt
                counter += 1
            else:
                end_pt -= 1

    return ans



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    inp = [[ln, sp, 0] for ln, sp in inp]

    def get_fit_block(ind, sz):
        pt = len(inp) - 1
        while pt > ind:
            if inp[pt][0] == 0 or inp[pt][0] > sz:
                pt -= 1
            elif inp[pt][0] <= sz:
                used = inp[pt][0]
                inp[pt][0] = 0
                inp[pt][2] = used
                return used, pt
        return None


    updated_disk = []

    for ind, item in enumerate(inp):
        ln, space, ex = item
        if ln:
            updated_disk.append((ind, ln))
        elif ex:
            updated_disk.append((None, ex))

        while space:
            res = get_fit_block(ind, space)
            if res is None:
                break
            used, bk_ind = res
            space -= used
            updated_disk.append((bk_ind, used))

        if space:
            updated_disk.append((None, space))
    
    ans = 0
    counter = 0
    for item in updated_disk:
        ind, ln = item
        if ind is not None:
            ans += ind*(counter*ln + sum_first_n(ln-1))

        counter += ln
            
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
