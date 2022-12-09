##### import utils, sys, re
import functools
from itertools import product

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
#data = utils.readfile("data/d09.txt")
poisitions = []
def tail_move(xh, yh, xt, yt, orient, count):
    coeff = {"L":[-1,0], "U":[0,1], "R":[1,0], "D":[0,-1]}
    xh += count*coeff[orient][0]
    yh += count*coeff[orient][1]
    move_n = 0
    while abs(yt-yh)+abs(xt-xh) > 1:
        move_n += 1
        if yt != yh:
            yt += (yh-yt)//abs(yh-yt)
        if xt != xh:
            xt += (xh-xt)//abs(xh-xt)
        positions[]
    return xh, yh, xt, yt, move_n
    
    
assert tail_move(0, 0, 0, 0, "L", 1) == (-1, 0, 0, 0, 0)
assert tail_move(0, 0, 0, 0, "U", 1) == (0, 1, 0, 0, 0)
assert tail_move(0, 0, 0, 0, "R", 1) == (1, 0, 0, 0, 0)
assert tail_move(0, 0, 0, 0, "D", 1) == (0, -1, 0, 0, 0)

assert tail_move(0, 0, 0, 0, "U", 3) == (0, 3, 0, 2, 2)

def d091(data):
    xh, yh, xt, yt = 0,0,0,0
    movements = 0
    for line in data:
        print(line)
        orient, coeff = line.split(" ")
        xh, yh, xt, yt, move_n = tail_move(xh,yh,xt,yt,orient,int(coeff))
        movements += move_n
    print("moves", movements)
    return movements
        
res = d091(data_ex)
print(res)

res = d092(data)
print(res)
            
