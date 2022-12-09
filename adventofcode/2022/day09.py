##### import utils, sys, re
import functools
from itertools import product

def pf(k):
    [i,j] = k.split('.')
    return int(i), int(j)
def fp(i,j):
    return str(i) + '.' + str(j)

data_ex=[
    "R 4",
    "U 4",
    "L 3",
    "D 1",
    "R 4",
    "D 1",
    "L 5",
    "R 2"
]
data = utils.readfile("data/d09.txt")

def tail_move(xh, yh, xt, yt, orient, count):
    coeff = {"L":[-1,0], "U":[0,1], "R":[1,0], "D":[0,-1]}
    xh += count*coeff[orient][0]
    yh += count*coeff[orient][1]
    move_n = 0
    if abs(yt-yh)+abs(xt-xh) > 1 and not abs(yt-yh)*abs(xt-xh)==1:
        move_n += 1
        if yt != yh:
            yt += (yh-yt)//abs(yh-yt)
        if xt != xh:
            xt += (xh-xt)//abs(xh-xt)
    return xh, yh, xt, yt, move_n
    
    
assert tail_move(0, 0, 0, 0, "L", 1) == (-1, 0, 0, 0, 0)
assert tail_move(0, 0, 0, 0, "U", 1) == (0, 1, 0, 0, 0)
assert tail_move(0, 0, 0, 0, "R", 1) == (1, 0, 0, 0, 0)
assert tail_move(0, 0, 0, 0, "D", 1) == (0, -1, 0, 0, 0)

#assert tail_move(0, 0, 0, 0, "U", 1) == (0, 3, 0, 2, 2)


def d091(data):
    positions = {fp(0,0):1}
    xh, yh, xt, yt = 0,0,0,0
    movements = 0
    for line in data:
        orient, coeff = line.split(" ")
        for i in range(0,int(coeff)):
            xh, yh, xt, yt, move_n = tail_move(xh,yh,xt,yt,orient,1)
            movements += move_n
            positions[fp(xt,yt)] = 1
    print("moves", movements)
    print("positions", len(positions.keys()))
    return positions
        
pos1_ex = d091(data_ex)
res = d091(data)

data_exemple_2 = [
    "R 5",
    "U 8",
    "L 8",
    "D 3",
    "R 17",
    "D 10",
    "L 25",
    "U 20"
]

def d092(data):
    positions = {fp(0,0):1}
    knots = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]
    for line in data:
        orient, coeff = line.split(" ")
        for i in range(0,int(coeff)):
            for kid in range(0, len(knots)-1):               
                (xh,yh) = knots[kid]
                (xt,yt) = knots[kid+1]
                if kid == 0:
                    xh, yh, xt, yt, move_n = tail_move(xh,yh,xt,yt,orient,1)
                else:
                    xh, yh, xt, yt, move_n = tail_move(xh,yh,xt,yt,orient,0)
                knots[kid] = (xh,yh)
                knots[kid+1] = (xt,yt)
                if kid == 8:
                    positions[fp(xt,yt)] = 1
    print("positions 2", len(positions.keys()))
    print(positions)
    return positions

pos2_ex = d092(data_ex)
pos2_ex = d092(data_exemple_2)
res = d092(data)
