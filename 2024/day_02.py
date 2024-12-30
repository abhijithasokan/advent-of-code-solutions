from utils import aoc_comm, run_example
import os

from collections import Counter

# --- update day/ year for each challenge
settings = {
    'day' : 2,
    'year' : 2024,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions

EXAMPLE_INP = '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''

def parse_input(inp_content):
    inp_content = inp_content.strip()
    inp_content = inp_content.split('\n')
    for line in inp_content:
        yield list(map(int, line.split()))
    
    
@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    reports = parse_input(input_str)
    safe_reports = 0
    for report in reports:
        safe_reports += 1
        inc = report[0] < report[1]
        diff_range = range(1, 4) if inc else range(-3, 0) 
        for ind in range(1, len(report)):
            if (report[ind] - report[ind-1]) not in diff_range:
                safe_reports -= 1
                break
    
    return safe_reports



@aoc_comm(settings, level = 2)
def solve_l2(input_str): # input data will be passed to this as string 
    reports = parse_input(input_str)
    safe_reports = 0
    for report in reports:
        safe_reports += 1
        N = len(report)
        inc = 0
        for i in range(1, min(N, 4)):
            diff = report[i] - report[i-1]
            inc += 1 if diff > 0 else -1 
        
        inc = bool(inc > 0)

        violation_seen = False

        diff_range = range(1, 4) if inc else range(-3, 0) 

        ind = 1
        while ind < N:
            if (report[ind] - report[ind-1]) not in diff_range:
                if not violation_seen:
                    resolved = False
                    if ind == N - 1:
                        # ignore the last violation
                        resolved = True
                    else:
                        if (report[ind+1] - report[ind-1]) in diff_range:
                            # throw out current element
                            resolved = True
                            ind += 1
                        else:
                            if ind == 1:
                                # just ignore the first
                                resolved = True
                            elif ( (report[ind] - report[ind-2]) in diff_range ):
                                # throw out the prev element
                                resolved = True
                        
                    if not resolved:
                        safe_reports -= 1
                        break
                     
                    violation_seen = True
                else:
                    safe_reports -= 1
                    break

            ind += 1
            
    return safe_reports



def main():
    print("Example 1 result: ", run_example(solve_l1, EXAMPLE_INP))
    l1_status = solve_l1()
    print(l1_status)

    print("Example 2 result: ", run_example(solve_l2, EXAMPLE_INP))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
