import utils, sys, re
import functools
from itertools import product

data_ex=[
    "30373",
    "25512",
    "65332",
    "33549",
    "35390"
]
data = utils.readfile("data/d08.txt")
for line in data_ex:
    print(line)

def pf(k):
    [i,j] = k.split('.')
    return int(i), int(j)
def fp(i,j):
    return str(i) + '.' + str(j)

def parse_tree(data):
    maptree = {}
    for i,line in enumerate(data):
        for j,height in enumerate(line):
            maptree[fp(i,j)]=int(height)
    return maptree

def other_trees(i,j,maptree):
    maxi,maxj=pf(max(maptree.keys()))
    other = [
        list(product(range(0,i), [j]))[::-1],
        list(product(range(i+1,maxi+1), [j])),
        list(product([i], range(0,j)))[::-1],
        list(product([i], range(j+1,maxj+1)))
    ]
    #print(other)
    return other

exemple = parse_tree(["00000","01110","01210","01110","00000"])
res = other_trees(2,2,exemple)
print(res)
assert(res) == [
    [(1, 2), (0, 2)], 
    [(3, 2), (4, 2)], 
    [(2, 1), (2, 0)], 
    [(2, 3), (2, 4)]
]

def d081(data):
    maptree = parse_tree(data)
    maxi,maxj=pf(max(maptree.keys()))
    visible_tree = maxi*2 + maxj*2
    for (x,y) in list(product(range(1, maxi), range(1, maxj))):
        others = other_trees(x,y,maptree)
        height = maptree[fp(x,y)]
        visible = True
        for side in others:
            visible = True
            for (u,v) in side:
                if maptree[fp(u,v)] >=height:
                    visible = False
                    break
            if visible:
                break
        if visible: 
            visible_tree += 1
    return visible_tree
        
res = d081(data_ex)
print(res)

res = d081(data)
print(res)

def d082(data):
    op = 0
    maptree = parse_tree(data)
    maxi,maxj=pf(max(maptree.keys()))
    maxview = 0
    for (x,y) in list(product(range(1, maxi), range(1, maxj))):
        others = other_trees(x,y,maptree)
        op += 1
        height = maptree[fp(x,y)]
        print("xy", x, y, "height", height)
        theview=1
        for side in others:
            if theview == 0:
                break
            sideview=0
            for (u,v) in side:
                op += 1
                sideview += 1
                #print("Ot : ", u,v,maptree[fp(u,v)])
                if maptree[fp(u,v)] >= height:
                    theview = theview*sideview
                    break
            theview=theview*sideview
        if theview
        maxview = max(maxview, theview)
    print("operations", op)
    return maxview

        
res = d082(data_ex)
print(res)

#res = d082(data)
#print(res)
            
