import json, re, time
from collections import Counter
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

def pf(k):
    #print(k)
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)

def getmap(maps, x, y):
    coord = fp(x,y)
    if not coord in maps.keys():
        return "."
    return maps[coord]

def printmap(maps):
    maxy = max([pf(k)[1] for k in maps.keys()])
    for y in range(maxy+1,0,-1):
        line = ""
        for x in range(0,7):
            line += getmap(maps,x,y)
        print(line)
        
data_ex = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
data = readfile("d17.txt")[0]

def get_shape(i):
    if i%5 == 0:
        return ["####"]
    if i%5 == 1:
        return [".#.","###",".#."]
    if i%5 == 2:
        return ["###","..#","..#"]
    if i%5 == 3:
        return ["#","#","#","#"]
    if i%5 == 4:
        return ["##","##"]
        
def move_block(maps, x, y, i, o):
    l = 7
    dx = x
    dy = y
    if o == 0:
        dy -= 1
    else:
        dx += o
    move = True
    for ny,line in enumerate(get_shape(i)):
        if x+len(line)>l:
            # Figure a l'exté dès le départ
            return False
        if x+len(line)+o > l or x+o < 0:
            #print("-> on sides")
            return maps, x, y, False
        for nx,char in enumerate(line):
            if char == "#":
                nmov = getmap(maps,nx+dx,ny+dy) == "."
                move = move and nmov
    if not move:
        if o == 0:
            #print("PAS descendu")
            for ny,line in enumerate(get_shape(i)):
                for nx,char in enumerate(line):
                    if char == "#":
                        maps[fp(nx+x,ny+y)] = "X"
            return maps,0,0,False
        else:
            #print("-> stuck left right")
            return maps, x, y, False
    return maps, dx, dy, True
    
assert move_block({}, 0, 0, 0, 1) == ({}, 1, 0, True)
assert move_block({}, 2, 0, 0, 1) == ({}, 3, 0, True)
assert move_block({}, 3, 0, 0, 1) == ({}, 3, 0, False)
assert move_block({}, 4, 0, 0, 1) == False
assert move_block({}, 0, 0, 0, -1) == ({}, 0, 0, False)
assert move_block({}, 1, 0, 0, -1) == ({}, 0, 0, True)

def block_at(x,y,i):
    themap = {}
    for ny,line in enumerate(get_shape(i)):
        for nx,char in enumerate(line):
            if char == "#":
                themap[fp(x+nx,y+ny)]="@"
    return themap

assert block_at(1,10,0) == {'1,10': '@', '2,10': '@', '3,10': '@', '4,10': '@'}
assert block_at(1,10,2) == {'1,10': '@', '2,10': '@', '3,10': '@', '3,11': '@', '3,12': '@'}
    
def d171(data):
    print("*" * 23)
    print("*" * 23)
    print("*" * 23)
    print("*" * 23)
    maps = {fp(i,0):"-" for i in range(0,8)}
    i = 0
    y = 4
    x = 2
    keep = True
    precedi = 0
    precedy = 0
    nnn = 0
    while keep:
        nnn += 1
        print("iteration", i, i-precedi, "\t", y-4, y-4-precedy)
        precedi = i
        precedy = y-4
        if nnn > 20:
            return False
        for push in data:
            #if i == 1585:
            #    return max([pf(k)[1] for k in maps.keys()])
            maps,x,y,r = move_block(maps, x, y, i, 1 if push==">" else -1)

            maps,x,y,r = move_block(maps, x, y, i, 0)

            if not r:
                i+=1
                x=2
                y=max([pf(k)[1] for k in maps.keys()]) + 4

            #blockat = block_at(x,y,i)
            #printmap({**maps, **blockat})    


susu = 1000000000000 - 14
print(susu)
r = susu//(8+7+7+7+6)
print(r)
leav = susu%(8+7+7+7+6)
print("leav",leav)
n = r * (15+9+14+7+8) + 21
diff = 1514285714288 - n
print("diff",diff)
nnn = r*(8+7+7+7+6)+14
print("n ", n, n%5)
print(n + 1)
print(n + 2)
print(n + 3)
print(n + 4)

maxex = d171(data_ex)

susu = 1000000000000 - 1740
print(susu)
r = susu//1725
print(r)
leav = susu%1725
print("leav",leav)
n = r * 1725 + 1740 + 1585
print("n ", n)

nnn = r * 2659 + 2677 + 2449

print(nnn)
print(nnn + 1)
print(nnn + 2)
print(nnn + 3)
print(nnn + 4)
#-- 1541449272704
#-- 1541449272705 too short

#   1541449275361
#-- 1541449275362
#-- 1541449275363
#   1541449275364
#   1541449275365
#   1541449275366
#-- 1541449275367
#   1541449275368
#   1541449275369
#   1541449275370
#   1541449275371

print(d171(data))
    
