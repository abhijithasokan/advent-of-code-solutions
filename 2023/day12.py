from utils import aoc_comm
import os

# --- update day/year for each challenge
settings = {
    'day' : 12,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions
def parse_input(inp_content):
    inp_content = list(inp_content.strip().split('\n'))
    for line in inp_content:
        pat, nums = line.split(' ')
        yield pat, list(map(int, nums.split(',')))

    


def solve(pat, nums):
    cont_any_to_right = [0]*len(pat)

    count_any =  0
    for ind, ch in reversed(list(enumerate(pat))):
        if ch == '.':
            count_any = 0
        else:
            count_any += 1
            
        cont_any_to_right[ind] = count_any

    last_ind = pat.rfind('#')

    memo = {}
    def solve2(pat_ind, fit_ind):
        key = (pat_ind, fit_ind)
        mem = memo.get(key, None)
        if mem is not None:
            return int(mem)
        
        if fit_ind == len(nums):
            if pat_ind > last_ind:
                return 1
            return 0
        
        if pat_ind >= len(pat):
            return 0

        bk_sz = nums[fit_ind]

        ans = 0
        if cont_any_to_right[pat_ind] >= bk_sz:
            if (pat_ind + bk_sz == len(pat)) or pat[pat_ind + bk_sz] != '#':
                ans = solve2(pat_ind + bk_sz + 1, fit_ind + 1) # fit this here
                
        if pat[pat_ind] != '#':
            ans += solve2(pat_ind+1, fit_ind) # also try to fit later indices

        memo[key] = ans
        return ans
 
    ans = solve2(0, 0)   
    return ans



@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    inp = parse_input(input_str)
    ans = 0
    for pat, nums in inp:
        ans += solve(pat, nums)

    return ans

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    ans = 0
    for pat, nums in inp:
        ans += solve('?'.join([pat]*5), nums*5)
    return ans


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
