from utils import aoc_comm
import os


# --- update day/ year for each challenge
settings = {
    'day' : 5,
    'year' : 2023,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}

# -- OTHER LIBs that might help while coding the soultions


def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n\n')
    seeds = map(int, inp_content[0].split(' ')[1:])

    maps = {}
    link_map = {}
    for maps_str in inp_content[1:]:
        maps_str = maps_str.split('\n')

        map_name = maps_str[0]
        map_name = map_name[:map_name.find('-')] 
        dest_map_name = maps_str[0]
        link_map[map_name] = dest_map_name[dest_map_name.find('to-')+3:dest_map_name.find(' ')]


        table = []
        for line in maps_str[1:]:
            dest, src, rng = list(map(int, line.split(' ')))
            table.append((Range(start=src, end=src+rng-1), dest-src))

        maps[map_name] = table

    return seeds, maps, link_map



class Range:
    def __init__(self, start, end):
        self.start, self.end = start, end

    def is_covering(self, other):
        rng = range(self.start, self.end+1)
        return other.start in rng and other.end in rng

    def has_overlap(self, other):
        rng = range(self.start, self.end+1) 
        return (other.start in rng) or (other.end in rng) or other.is_covering(self) 


    @staticmethod
    def clean_range(rngs):
        return [rng for rng in rngs if rng.start <= rng.end]

    '''
        returns a list of range.
        the first item corresponds to overlapping region with self
    '''
    def break_range(self, other):
        if self.is_covering(other):
            return [other]
        
        if other.is_covering(self):
            return Range.clean_range([self, Range(other.start, self.start-1), Range(self.end+1, other.end)])
        
        if other.start < self.start:
            return Range.clean_range([Range(self.start, other.end), Range(other.start, self.start-1)])

        return Range.clean_range([Range(other.start, self.end), Range(self.end+1, other.end)])


    def shift(self, offset):
        return Range(self.start+offset, self.end+offset)
    
    def __repr__(self):
        return f'Range({self.start}, {self.end})'

    def __str__(self):
        return repr(self)


def lookup(window, table):
    windows = [window]
    processed = []

    for rng, offset in table:
        new_windows = []
        for window in windows:
            if rng.has_overlap(window):
                overlap, *others = rng.break_range(window)
                processed.append(overlap.shift(offset)) # already mapped
                new_windows.extend(others) # broken ranges
            else:
                new_windows.append(window)
        windows = new_windows

    processed.extend(windows)
    return processed


def traverse(link_map, maps, items):
    cur_map = 'seed'
    
    while cur_map in link_map:
        mapped_items = []
        for item in items:
            mapped_items.extend(lookup(item, maps[cur_map]))
        cur_map = link_map[cur_map]
        items = mapped_items

    return items




@aoc_comm(settings, level = 1)
def solve_l1(input_str):
    seeds, maps, link_map = parse_input(input_str)
    seeds = list(seeds)
    new_seeds = [Range(seed, seed) for seed in seeds]

    locs = traverse(link_map, maps, new_seeds)
    min_loc = min(rng.start for rng in locs)

    return min_loc



@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    seeds, maps, link_map = parse_input(input_str)
    seeds = list(seeds)
    new_seeds = []
    for seed, num in zip(seeds[::2], seeds[1::2]):
        new_seeds.append(Range(seed, seed+num-1))

    locs = traverse(link_map, maps, new_seeds)
    min_loc = min(rng.start for rng in locs)

    return min_loc




def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
