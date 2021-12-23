import copy
from utils import aoc_comm
import os
from collections import defaultdict
import heapq
import itertools


settings = {
    'day' : 23,
    'year' : 2021,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

COST_MAP = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
AMPHIPOD_CHARS = 'ABCD'


def parse_input(inp_content, extra_lines=[]):
    inp_content = inp_content.strip().split('\n')[1:-1]
    hallway_line, room_lines = inp_content[0][1:-1], inp_content[1:]
    hallway = list(itertools.chain(hallway_line[:2], hallway_line[3:-2:2], hallway_line[-2:]))
    room_lines = itertools.chain([room_lines[0]], extra_lines, room_lines[1:])
    room_data = [line.strip().replace('##', '')[1:-1].split('#') for line in room_lines]
    rooms = list(list(reversed(rm_data)) for rm_data in zip(*room_data))
    return hallway, rooms


class GraphData:
    def __init__(self):
        self.state_to_id = {}
        self.id_to_state = {}
        self.dest_states = set()
        self.visited_nodes = set()
        self.adj_mat = defaultdict(dict)


def get_key(hallway, rooms, gph_data):
    key_ss = ''.join(hallway) + ''.join(''.join(room) for room in rooms)
    node_id = gph_data.state_to_id.get(key_ss, None)
    if node_id is not None:
        return node_id
    node_id = len(gph_data.state_to_id)
    gph_data.state_to_id[key_ss] = node_id
    gph_data.id_to_state[node_id] = (hallway.copy(), copy.deepcopy(rooms))
    return node_id


def make_move_and_add_node(h_id, room_id, seat, hallway, rooms, node_id, cost, gph_data, new_states):
    hallway[h_id], rooms[room_id][seat] = rooms[room_id][seat], hallway[h_id]
    next_node_id = get_key(hallway, rooms, gph_data)
    gph_data.adj_mat[node_id][next_node_id] = cost
    hallway[h_id], rooms[room_id][seat] = rooms[room_id][seat], hallway[h_id]

    if next_node_id not in gph_data.visited_nodes:
        new_states.add(next_node_id)


def get_hallway_ids_and_dist(hallway, room_id):
    for h_id in reversed(range(0, room_id+2)):
        if hallway[h_id] != '.':
            break
        yield h_id, abs(h_id-(room_id+1))*2 + 1 - (1 if h_id == 0 else 0)
    for h_id in range(room_id+2, len(hallway)):
        if hallway[h_id] != '.':
            break
        yield h_id, abs(h_id-(room_id+2))*2 + 1 - (1 if h_id == (len(hallway)-1) else 0)


def move_out(room_id, seat, hallway, rooms, node_id, gph_data, new_states):
    if rooms[room_id][seat].islower():  # already placed
        return
    if not all_equal(rooms[room_id][seat+1:], '.'):  # no way to move out
        return
    num_seats = len(rooms[room_id])
    for h_id, hall_dist in get_hallway_ids_and_dist(hallway, room_id):
        steps = (num_seats - seat) + hall_dist
        move_cost = COST_MAP[rooms[room_id][seat]] * steps
        make_move_and_add_node(h_id, room_id, seat, hallway, rooms, node_id, move_cost, gph_data, new_states)


def move_in(h_id, hallway, rooms, node_id, gph_data, new_states):
    orig_hid = h_id
    unit_cost = COST_MAP[hallway[orig_hid]]
    is_end_hallway = (h_id == 0 or h_id == len(hallway)-1)
    h_id = abs(h_id - (1 if is_end_hallway else 0))

    room_id = ord(hallway[orig_hid]) - ord('A')
    dest_hall_id = room_id + (1 if abs(room_id+1-h_id) < abs(room_id+2-h_id) else 2)

    if dest_hall_id > orig_hid:
        if not all_equal(hallway[orig_hid+1:dest_hall_id+1], '.'):
            return
    elif not all_equal(hallway[dest_hall_id:orig_hid], '.'):
        return

    steps = abs(dest_hall_id - h_id) * 2 + 1 + (1 if is_end_hallway else 0)
    for seat_id in range(len(rooms[room_id])):
        if all_equal(rooms[room_id][seat_id:], '.') and all_equal(rooms[room_id][:seat_id], hallway[orig_hid].lower()):
            hallway[orig_hid] = hallway[orig_hid].lower()
            move_cost = unit_cost * (steps + (len(rooms[room_id]) - seat_id))
            make_move_and_add_node(orig_hid, room_id, seat_id, hallway, rooms, node_id, move_cost, gph_data, new_states)
            hallway[orig_hid] = hallway[orig_hid].upper()
            break
    return


def all_equal(lst, key = None):
    if not lst or len(lst) == 0:
        return True
    if key is None:
        key = lst[0]
    return lst.count(key) == len(lst)


def is_dest_node(hallway, rooms):
    return all_equal(hallway, '.') and all(all_equal(rooms[ind], item) for ind, item in enumerate('abcd'))


def simulate_node(hallway, rooms, gph_data, new_states):
    node_id = get_key(hallway, rooms, gph_data)
    gph_data.visited_nodes.add(node_id)
    if is_dest_node(hallway, rooms):
        gph_data.dest_states.add(node_id)
        return

    for room_id in range(len(rooms)):
        for seat_id in range(len(rooms[room_id])):
            if rooms[room_id][seat_id] != '.':
                move_out(room_id, seat_id, hallway, rooms, node_id, gph_data, new_states)

    for hall_id in range(len(hallway)):
        if hallway[hall_id] != '.':
            move_in(hall_id, hallway, rooms, node_id, gph_data, new_states)


def simulate(hallway, rooms, gph_data):
    new_states = set()
    simulate_node(hallway, rooms, gph_data, new_states)
    while new_states:
        next_states = set()
        for node_id in new_states:
            hways, rms = gph_data.id_to_state[node_id]
            simulate_node(hways, rms, gph_data, next_states)
        new_states = next_states


def shortest_dist(gph_data):
    adj_mat, end_nodes, sz = gph_data.adj_mat, gph_data.dest_states, len(gph_data.state_to_id)
    pq = [(0, 0)]
    dists, visited = [None]*sz, set()
    while pq:
        dd, node = heapq.heappop(pq)
        if node in end_nodes:
            return dd
        if node in visited:
            continue
        visited.add(node)
        for adj_node, wt in adj_mat[node].items():
            if (dists[adj_node] is None) or (dists[adj_node] > dd + wt):
                dists[adj_node] = dd + wt
                heapq.heappush(pq, (dists[adj_node], adj_node))
    return


def mark_fixed(rooms):
    for room_id, ch in enumerate(AMPHIPOD_CHARS):
        for ind in range(len(rooms[room_id])):
            if rooms[room_id][ind] != ch:
                break
            rooms[room_id][ind] = rooms[room_id][ind].lower()
    return


def get_min_cost(hallway, rooms):
    mark_fixed(rooms)
    gph_data = GraphData()
    simulate(hallway, rooms, gph_data)
    return shortest_dist(gph_data)


@aoc_comm(settings, level=1)
def solve_l1(input_str):
    hallway, rooms = parse_input(input_str)
    return get_min_cost(hallway, rooms)


@aoc_comm(settings, level=2)
def solve_l2(input_str):
    hallway, rooms = parse_input(input_str, extra_lines=['#D#C#B#A#', '#D#B#A#C#'])
    return get_min_cost(hallway, rooms)


def main():
    l1_status = solve_l1()
    print(l1_status)
    l2_status = solve_l2()
    print(l2_status)
    return


if __name__ == '__main__':
    main()

