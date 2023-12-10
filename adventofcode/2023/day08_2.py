import sys, re, time, numpy, collections, numpy

def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content


data_ex= [
    "RL",
    "",
    "AAA = (BBB, CCC)",
    "BBB = (DDD, EEE)",
    "CCC = (ZZZ, GGG)",
    "DDD = (DDD, DDD)",
    "EEE = (EEE, EEE)",
    "GGG = (GGG, GGG)",
    "ZZZ = (ZZZ, ZZZ)"
]
data_ex_2 = [
    "LLR",
    "",
    "AAA = (BBB, BBB)",
    "BBB = (AAA, ZZZ)",
    "ZZZ = (ZZZ, ZZZ)"
]
data_ex_3 = [
    "LR",
    "",
    "11A = (11B, XXX)",
    "11B = (XXX, 11Z)",
    "11Z = (11B, XXX)",
    "22A = (22B, XXX)",
    "22B = (22C, 22C)",
    "22C = (22Z, 22Z)",
    "22Z = (22B, 22B)",
    "XXX = (XXX, XXX)"
]
data = readfile("data/d_2023_08.txt")

def get_pathfinder(data):
    pathfinder = {}
    
    for line in data:
        rex = re.search("([0-9A-Z]+) = \(([0-9A-Z]+), ([0-9A-Z]+)\)", line)
        pathfinder[rex.groups()[0]] = rex.groups()[1:3]
    return pathfinder

def day08(data):
    pos = "AAA"
    endpos = "ZZZ"
    path = [c for c in data[0]]
    pathfinder = get_pathfinder(data[2:])
    startpos = pos
    startpath = path
    direction = {'L':0, 'R':1}
    count = 0
    
    while True:
        next_direction, path = path[0], path[1:]
        if len(path) == 0:
            path = startpath
        
        pos = pathfinder[pos][direction[next_direction]]
        #print('POS', pos)
        count += 1
        if pos == endpos:
            #print("count", count)
            return count    
        if pos == startpos and path == startpath:
            raise Exception('LOOP')

def day08_b(data):
    start = time.time()
    path = [c for c in data[0]]
    startpath = path
    print("path", len(startpath))
    pathfinder = get_pathfinder(data[2:])
    
    ghost_pos = [a_path for a_path in pathfinder.keys() if a_path[-1] == 'A']
    print('START POS', ghost_pos)
    direction = {'L':0, 'R':1}
    count = 0
    
    freq_ghosts = [{'start':pos, 'z':{}, 'loop':0} for pos in ghost_pos]
    OK_ghosts = []
    nb_ghosts = len(ghost_pos)
    
    while len(OK_ghosts) != nb_ghosts :            
        next_direction, path = path[0], path[1:]
        next_pos = []
        if count in [267,268,269]:
            print(ghost_pos)
            print(path)
        for i,pos in enumerate(ghost_pos):
            next_pos.append( pathfinder[pos][direction[next_direction]] )
            if not i in OK_ghosts:
                if pos[-1] == 'Z':
                    keyuniq = pos +'@'+ str(len(path))
                    if keyuniq in freq_ghosts[i]['z']:
                        freq_ghosts[i]['loop'] = (count - freq_ghosts[i]['z'][keyuniq], freq_ghosts[i]['z'][keyuniq])
                        OK_ghosts.append(i)
                    else:
                        freq_ghosts[i]['z'][keyuniq] = count
    
        ghost_pos = list(set(next_pos))
        if len(path) == 0:
            path = startpath
        #print('POS', ghost_pos)
        count += 1
    coeffs = []
    right = []
    
    numbers = []
    for n,ghost in enumerate(freq_ghosts):
        print(ghost)
    
    

assert day08(data_ex) == 2
assert day08(data_ex_2) == 6
start = time.time()
print("result", day08(data))
end = time.time()
print("Time : ", int(end - start), "s")

r= day08_b(data_ex_3)
start = time.time()
print("result", day08_b(data))
end = time.time()
print("Time : ", int(end - start), "s")

ppcm
