import utils, sys, re
import time, numpy, collections, itertools

data_ex= [
    "O....#....",
    "O.OO#....#",
    ".....##...",
    "OO.#O....O",
    ".O.....O#.",
    "O.#..O.#.#",
    "..O..#O..O",
    ".......O..",
    "#....###..",
    "#OO..#...."
]
data = utils.readfile("data/d_2023_14.txt")

def ij2k(i,j): 
    return str(i)+'.'+str(j)
def k2ij(k):
    (i,j) = tuple(map(int, k.split('.')))
    return i,j 
def get_rock(i,j,map_rock):
    return map_rock.get(ij2k(i,j), '.')
def set_rock(i,j,map_rock,value):
    k = ij2k(i,j)
    if value == '.':
        if k in map_rock:
            del map_rock[k]
    else:
        map_rock[k] = value
    return map_rock
    
def get_max_map_rock(map_rock):
    max_i = max(map(lambda x: int(x.split('.')[0]), map_rock.keys()))
    max_j = max(map(lambda x: int(x.split('.')[1]), map_rock.keys()))
    
    return max_i, max_j

def tilt(map_rock, direction):
    max_i, max_j = get_max_map_rock(map_rock)
    #print(max_i, "x", max_j)
    rock_lines = {
        'N': [[(i,j,-1, 0) for j in range(0, max_j+1)] for i in range(0, max_i+1)],
        'S': [[(i,j, 1, 0) for j in range(0, max_j+1)] for i in range(max_j, -1, -1)],
        'W': [[(i,j, 0,-1) for i in range(0, max_i+1)] for j in range(0, max_j+1)],
        'E': [[(i,j, 0, 1) for i in range(0, max_i+1)] for j in range(max_j, -1, -1)],
    }
    for rock_line in rock_lines[direction]:
        for (ri, rj, di, dj) in rock_line:
            if get_rock(ri, rj, map_rock) == 'O':
                keep_rolling = True
                while keep_rolling:
                    if (0 <= ri+di <= max_i and 0 <= rj+dj <= max_j 
                        and get_rock(ri+di, rj+dj, map_rock) == '.'):
                        map_rock = set_rock(ri, rj, map_rock, '.')
                    else:
                        map_rock = set_rock(ri, rj, map_rock, 'O')
                        keep_rolling = False
                    ri = ri+di
                    rj = rj+dj
    return map_rock


def parse_map_rock(data):
    map_rocks = {}
    for i,line in enumerate(data):
        for j,c in enumerate(line):
            if c in ['#', 'O']:
                map_rocks[ij2k(i,j)] = c
    print(map_rocks)
    return map_rocks

def print_map_rock(map_rock):
    print("*"*20)
    max_i, max_j = get_max_map_rock(map_rock)
    for i in range(0, max_i+1):
        line = ""
        for j in range(0, max_j+1):
            line += get_rock(i,j, map_rock)
        print(line)
    print("*"*20)

def get_load_map_rock(map_rock):
    max_i, max_j = get_max_map_rock(map_rock)
    load = 0
    for i in range(0, max_i+1):
        for j in range(0, max_j+1):
            rock = get_rock(i, j, map_rock)
            if rock == 'O':
                load += max_i + 1 - i
    print(load)
    return load
        
    
    
def day14(data):
    map_rock = parse_map_rock(data)
    print_map_rock(map_rock)
    map_rock = tilt(map_rock, 'N')
    
    print_map_rock(map_rock)

    return get_load_map_rock(map_rock)
    
assert day14(data_ex) == 136

start = time.time()
print("result", day14(data))
end = time.time()
print("Time : ", (end - start)*1000, " ms")

def day14_B(data):
    maxn = 1000000000
    map_rock = parse_map_rock(data)
    
    pastpos = {}
    keep = True
    n = 0
    loop = 0
    looped = False
    while n < maxn:
        if n % 10000 == 0:
            print(n)
        map_rock = tilt(map_rock, 'N')
        map_rock = tilt(map_rock, 'W')
        map_rock = tilt(map_rock, 'S')
        map_rock = tilt(map_rock, 'E')
        n += 1
        keys = [k for k,r in map_rock.items() if r == 'O']
        strkey = '-'.join(sorted(keys))
        if strkey in pastpos and not looped:
            print(f"Loop hole in {n} - so {pastpos[strkey]}")
            loop = (n - pastpos[strkey])
            n = (((maxn- pastpos[strkey]) // loop) * loop) + pastpos[strkey] - loop
            print(f"changed into {n}")
            looped = True
        else:
            pastpos [strkey ] = n
    return get_load_map_rock(map_rock)
    
assert day14_B(data_ex) == 64

start = time.time()
print("result", day14_B(data))
end = time.time()
print("Time : ", (end - start)*1000, " ms")

