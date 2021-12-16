from utils import aoc_comm
import os
import functools
import operator

# --- update day/ year for each challenge
settings = {
    'day' : 16,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


example_inp='''9C0141080250320F1802104A08'''

def parse_num(ss):
    blocks = [ss[i:i + 5] for i in range(0, len(ss), 5)]
    num_b = ''
    # print(blocks)
    read_c = 0
    for bk in blocks:
        num_b = num_b + bk[1:]
        read_c += len(bk)
        if bk[0] == '0':
            break
    number = int(num_b, 2)
    return number, read_c

def solve(ss):
    bin_ss = ''.join(bin(int(e, 16))[2:].zfill(4) for e in ss)
    parent = []
    parse_packets(bin_ss, parent)
    print(parent)
    return parent

def parse_packets(bin_ss, parent):
    if len(bin_ss) < 7:
        return len(bin_ss)

    version = int(bin_ss[:3], 2)
    type = int(bin_ss[3:6], 2)
    offset = 6
    if type == 4: # literal
        rem = bin_ss[offset:]
        number, read_c = parse_num(rem)
        #print("number: ", number)
        offset += read_c
        parent.append((version, type, number))
        offset += parse_packets(bin_ss[offset:], parent)
    else:
        # if len(bin_ss) < 7:
        #     return 6
        len_type = bin_ss[6]
        offset += 1
        res = (version, type, [])
        if len_type == '0':
            char_len = int(bin_ss[offset:offset+15], 2)
            offset += 15
            parse_packets(bin_ss[offset:offset+char_len], res[-1])
            offset += char_len
            parent.append(res)
            offset += parse_packets(bin_ss[offset:], parent)
        else:
            num_packets = int(bin_ss[offset:offset + 11], 2)
            offset += 11
            ff = []
            offset += parse_packets(bin_ss[offset:], ff)
            res[-1].extend(ff[:num_packets])
            parent.append(res)
            parent.extend(ff[num_packets:])

    return offset


def clean(packets):
    sum = 0
    for ver, _, sub_packets in packets:
        sum += ver
        if isinstance(sub_packets, list):
            sum += sum_versions(sub_packets)
    return sum

def sum_versions(packets):
    sum = 0
    for ver, _, sub_packets in packets:
        sum += ver
        if isinstance(sub_packets, list):
            sum += sum_versions(sub_packets)
    return sum


def parse_input(inp_content):
    inp_content = inp_content.strip()
    return inp_content



@aoc_comm(settings, level = 1)
def solve_l1(input_str): # input data will be passed to this as string 
    inp = parse_input(input_str)
    packets = solve(inp)
    return sum_versions(packets)



def calc(packet):
    val = 0
    ver, typ, sub_packets = packet
    if 1:
        if typ == 4:
            return sub_packets
        if typ == 0:
            val = sum(map(calc, sub_packets))
        elif typ == 1:
            val = functools.reduce(operator.mul, map(calc, sub_packets))
            #print("mul", val)
        elif typ == 2:
            val = min(map(calc, sub_packets))
        elif typ == 3:
            val = max(map(calc, sub_packets))
        elif typ == 5:
            sp1, sp2 = sub_packets
            val = int(calc(sp1) > calc(sp2))
        elif typ == 6:
            sp1, sp2 = sub_packets
            val = int(calc(sp1) < calc(sp2))
        elif typ == 7:
            sp1, sp2 = sub_packets
            val = int(calc(sp1) == calc(sp2))
    return val

@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    packets = solve(inp)
    return calc(packets[0])



def main():
    print("[L1] Ex: ", solve_l1.raw_(example_inp))
    l1_status = solve_l1()
    print(l1_status)


    print("[L2] Ex: ", solve_l2.raw_(example_inp))
    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
