import json, re
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_exo = readfile("data/d20.txt")
#print(data_exemple)
#print(data_exo)

def setorelse(tab, e, v = 1):
    if v == '#' or v == 1:
        tab[e] = 1
    elif v == '.' or v == 0:
        tab[e] = 0
    else:
        print(f"Exception {v}")
        raise Exception('Unattended')
    return tab

def pf(k):
    #print(k)
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)

algo = ( "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##" +
"#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###" +
".######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#." +
".#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#....." +
".#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.." +
"...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#....." +
"..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#" )

data_exemple = ["#..#.","#....","##..#","..#..","..###"]

def getmap(data):
    nmap = {}
    minaxs = {
        'i_a':0, 
        'i_z':len(data), 
        'j_a':0, 
        'j_z':len(data[0])
    }
    for i,line in enumerate(data):
        for j,cha in enumerate(line):
            setorelse(nmap, fp(i,j), cha)
    return nmap, minaxs

nmap, minaxs = getmap(data_exemple)

def applyit(nmap, minaxs, algo, defa=0):
    newmap = nmap.copy()
    coords = [(x,y) for x in [-1,0,1] for y in [-1,0,1]]
    minaxs['i_a']-=1
    minaxs['j_a']-=1
    minaxs['i_z']+=1
    minaxs['j_z']+=1
    #print(minaxs)
    for i in range(minaxs['i_a'], minaxs['i_z']):
        for j in range(minaxs['j_a'], minaxs['j_z']):
            bits = int(''.join([str(nmap.get(fp(i+x,j+y),defa)) for (x,y) in coords]), 2)
            newmap = setorelse(newmap,fp(i,j),algo[bits])
    print(len(list(filter(lambda x: x==1, newmap.values()))))
    return newmap, minaxs
                
for i in range(0,50):
    print(i) 
    nmap, minaxs = applyit(nmap, minaxs, algo)
    
print("###########")

algo = data_exo[0]
nmap, minaxs = getmap(data_exo[2:])
for i in range(0,50):
    defa = i%2
    print(i, defa) 
    nmap, minaxs = applyit(nmap, minaxs, algo, defa=defa)
