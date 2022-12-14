import utils, sys, re, numpy, json
import functools
from itertools import product

data_ex = [
    "498,4 -> 498,6 -> 496,6",
    "503,4 -> 502,4 -> 502,9 -> 494,9"
]
data = utils.readfile("data/d14.txt")    

def pf(k):
    #print(k)
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)

def getmap(mapw, x, y):
    coord = fp(x,y)
    if not coord in mapw.keys():
        return "."
    return mapw[coord]
    
def parse_waterfall(data):
    mapw = {}
    for line in data:
        pattern = ',| -> '
        points = re.split(pattern, line)
        for i in range(0, len(points)//2-1):
            a = int(points[i*2])
            b = int(points[i*2 + 1])
            x = int(points[(i+1)*2])
            y = int(points[(i+1)*2 + 1])
            for dx in range(min(a, x), max(a,x)+1):
                for dy in range(min(b,y), max(b,y)+1):
                    mapw[fp(dx,dy)] = "#"
    return mapw

print(parse_waterfall(["503,4 -> 502,4 -> 502,9"]))
print([i for i in range(10, 8, -1)])


def print_waterfall(mapw):
    ab = [pf(coo) for coo in mapw.keys()]
    minx = min([a for (a,b) in ab])
    maxx = max([a for (a,b) in ab])
    maxy = max([b for (a,b) in ab])
    print("-----------")
    rowstr=""
    for i in range(3,-1,-1):
        rowstr= " "*6
        for x in range(minx-3, maxx+4):
            rowstr+= str(x//10**(i)%10)
        print(rowstr)
    for y in range(0, maxy+4):
        rowstr = str(y).rjust(5) + " "
        for x in range(minx-3, maxx+4):
            rowstr += getmap(mapw, x,y)
        print(rowstr)

def add_sand(mapw, coord, maxy, stop = True):
    (x,y) = pf(coord)
    if getmap(mapw, x+1, y+1) != ".":
        return mapw, False
    keep = True
    while keep:
        nx = x
        ny = y
        if getmap(mapw, x, y+1) == ".":
            ny = y+1
        elif getmap(mapw, x-1, y+1) == ".":
            ny = y+1
            nx = x-1
        elif getmap(mapw, x+1, y+1) == ".":
            ny = y+1
            nx = x+1
        keep = (nx != x or ny != y)
        x = nx
        y = ny
        if y == maxy:
            mapw[fp(nx, ny)] = "o"
            return mapw, not stop
    mapw[fp(nx, ny)] = "o"
    return mapw, True
        
    
def d141(data):
    mapw = parse_waterfall(data)
    print(mapw)
    print_waterfall(mapw)
    
    ab = [pf(coo) for coo in mapw.keys()]
    maxy = max([b for (a,b) in ab])
    
    part1 = False
    
    nround = 0
    keep = True
    while keep:
        nround += 1
        if nround % 1000 == 0:
            print(nround)
        mapw, keep = add_sand(mapw, fp(500,0), maxy+1, part1)
        
        #print_waterfall(mapw)
    print_waterfall(mapw)
    print(nround, "grain de sable")
        
d141(data_ex)
d141(data)
