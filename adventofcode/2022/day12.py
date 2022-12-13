import utils, sys, re, numpy
import functools
from itertools import product

  
def pf(k):
    #print(k)
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)

data_ex = [
    "Sabqponm",
    "abcryxxl",
    "accszExk",
    "acctuvwj",
    "abdefghi"
]
data = utils.readfile("data/d12.txt")


def process(data):
    mapc = {}
    maxi = len(data)
    maxj = len(data[0])
    n0 = fp(0,0)
    ne = fp(0,0)
    
    print("MAXI", maxi, "MAXJ", maxj)
    for i,line in enumerate(data):
        for j, lett in enumerate(list(line)):
            if lett == "S":
                n0 = fp(i,j)
                lett = "a"
            if lett == "E":
                ne = fp(i,j)
                lett = "z"
            l = ord(lett)
            mapc[fp(i,j)] = l
    return mapc,maxi,maxj,n0,ne

def djikstra(mapc,maxi,maxj,node,nodeend, maxdiff):
    visited = {}
    distance = {}
    distance[node] = 0
    keep = True
    while keep:
        i,j = pf(node)
        #print("### START", i, j)
        #keep = False
        for (ni,nj) in [(i+1,j),(i,j+1), (i-1,j) ,(i,j-1)]:
            if ni<maxi and nj<maxj and ni>=0 and nj>=0:
                nkey = fp(ni,nj)            
                #print("chemin :", node, mapc[node], " vs ", nkey, mapc[nkey])
                if (mapc[nkey]-mapc[node])<=maxdiff:
                    if not nkey in visited:
                        ndist = distance[node] + 1
                        if not nkey in distance or ndist < distance[nkey]:
                            distance[nkey] = ndist
        visited[node] = distance[node]
        if node == nodeend:
            return node, distance[node]
        del distance[node]
        tdist = -1
        tnode = None
        #print(distance)
        for elnode,eldist in distance.items():
            #print(elnode, eldist)
            if tdist == -1 or eldist < tdist:
                tdist = eldist
                tnode = elnode
        if tnode == None:
            return None, 0
        node = tnode

def d121(data):
    mapc,maxi,maxj,node,nodeend = process(data)
    res = djikstra(mapc,maxi,maxj,node,nodeend, 1)
    print(res)

def d122(data):
    mapc,maxi,maxj,node,nodeend = process(data)
    nodes_a = [node for node,size in mapc.items() if size == ord("a")]
    print(nodes_a)
    distances = []
    for node in nodes_a:
        new_node,res = djikstra(mapc,maxi,maxj,node,nodeend, 1)
        if new_node != None:
            print(res)
            distances.append(res)
    print(min(distances))
    
d121(data_ex)
d121(data)

d122(data_ex)
d122(data)
