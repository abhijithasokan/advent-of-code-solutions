from utils import aoc_comm
import os
import functools
import operator

settings = {
    'day' : 16,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_num(ss):
    BLOCK_SIZE = 5
    blocks = (ss[i:i + BLOCK_SIZE] for i in range(0, len(ss), BLOCK_SIZE))
    num = 0
    read_c = 0
    for bk in blocks:
        num = (num << (BLOCK_SIZE - 1)) + int(bk[1:], 2)
        read_c += len(bk)
        if bk[0] == '0':
            break
    return num, read_c


def solve(ss):
    bin_ss = ''.join(bin(int(e, 16))[2:].zfill(4) for e in ss)
    packets = []
    parse_packets(bin_ss, packets)
    return packets


def parse_packets(bin_ss, parent):
    if len(bin_ss) < 7:
        return len(bin_ss)
    version, typ = int(bin_ss[:3], 2), int(bin_ss[3:6], 2)
    read_c = 6
    if typ == 4:  # literal
        number, rc = parse_num(bin_ss[read_c:])
        read_c += rc
        parent.append((version, typ, number))
        read_c += parse_packets(bin_ss[read_c:], parent)
    else:
        len_typ = bin_ss[6]
        read_c += 1
        res = (version, typ, [])
        if len_typ == '0':
            char_len = int(bin_ss[read_c:read_c+15], 2)
            read_c += 15
            parse_packets(bin_ss[read_c:read_c+char_len], res[-1])
            read_c += char_len
            parent.append(res)
            read_c += parse_packets(bin_ss[read_c:], parent)
        else:
            num_packets = int(bin_ss[read_c:read_c + 11], 2)
            read_c += 11
            ff = []
            read_c += parse_packets(bin_ss[read_c:], ff)
            res[-1].extend(ff[:num_packets])
            parent.append(res)
            parent.extend(ff[num_packets:])
    return read_c


def sum_versions(packet):
    version_sum = 0
    ver, _, sub_packets = packet
    version_sum += ver
    if isinstance(sub_packets, list):
        version_sum += sum(map(sum_versions, sub_packets))
    return version_sum


def parse_input(inp_content):
    return inp_content.strip()


def calc(packet):
    _, typ, sub_packets = packet

    def build_map_func(func):
        def ff(inp):
            return func(map(calc, inp))
        return ff

    def build_cmp_func(func):
        def ff(inp):
            return int(func(calc(inp[0]), calc(inp[1])))
        return ff

    typ_to_func = {
        0 : build_map_func(sum),
        1 : build_map_func(functools.partial(functools.reduce, operator.mul)),
        2 : build_map_func(min),
        3 : build_map_func(max),
        4 : (lambda x: x),
        5 : build_cmp_func(operator.gt),
        6 : build_cmp_func(operator.lt),
        7 : build_cmp_func(operator.eq),
    }
    return typ_to_func[typ](sub_packets)


@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    inp = parse_input(input_str)
    packets = solve(inp)
    return sum_versions(packets[0])


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    inp = parse_input(input_str)
    packets = solve(inp)
    return calc(packets[0])


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
