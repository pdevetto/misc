import utils, sys, re
import time, numpy, collections, itertools

data_ex= [
    "...#......",
    ".......#..",
    "#.........",
    "..........",
    "......#...",
    ".#........",
    ".........#",
    "..........",
    ".......#..",
    "#...#....."
]
data = utils.readfile("data/d_2023_11.txt")

def ij2k(i,j): 
    return str(i)+'.'+str(j)
def k2ij(k):
    (i,j) = tuple(map(int, k.split('.')))
    return i,j 
def distance_composante(t,u, empty_e={}, empty_size=2):
    if t == u:
        return 0
    delta = len([i for i in range(min(t,u), max(t,u)) if empty_e.get(i, False)])
    return abs(t - u) + delta * (empty_size-1)
        
assert distance_composante(1, 5, {2:True, 3:False}) == 5
assert distance_composante(1, 5, {2:True, 3:True}) == 6
assert distance_composante(5, 1, {2:True, 3:True}) == 6
assert distance_composante(1, 5) == 4

def distance_ab(a, b, empty_size=2, empty_rows={}, empty_cols={}):
    ia, ja = k2ij(a)
    ib, jb = k2ij(b)
    return (distance_composante(ia, ib, empty_rows, empty_size) + 
        distance_composante(ja, jb, empty_cols, empty_size))
    
assert distance_ab('1.1','3.3') == 4
assert distance_ab('1.1','3.3', 2, {2:True}, {2:True}) == 6
    
def day11(data, empty_size):
    map_galaxies = {}
    empty_cols = {col:True for col in range(0,len(data[0]))}
    empty_rows = {col:True for col in range(0,len(data))}
    galaxi = 0
    for i,line in enumerate(data):
        for j,c in enumerate(line):
            if c == '#':
                galaxi += 1
                empty_cols[j] = False
                empty_rows[i] = False
                map_galaxies[ij2k(i,j)] = str(galaxi)
    dists = {
        map_galaxies[pair[0]]+"x"+map_galaxies[pair[1]]: 
            distance_ab(pair[0], pair[1], empty_size, empty_rows, empty_cols) 
        for pair in list(itertools.combinations(map_galaxies.keys(), 2))
    }
    return sum(dists.values())

assert day11(data_ex, 2) == 374
start = time.time()
print("result", day11(data, 2))
assert day11(data, 2) == 10228230
end = time.time()
print("Time : ", (end - start)*1000, " ms")

assert day11(data_ex, 10) == 1030
assert day11(data_ex, 100) == 8410
start = time.time()
print("result", day11(data, 1000000))
end = time.time()
print("Time : ", (end - start)*1000, " ms")
