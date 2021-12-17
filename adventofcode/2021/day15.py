import utils, sys
data_exemple = ["1163751742",
"1381373672",
"2136511328",
"3694931569",
"7463417111",
"1319128137",
"1359912421",
"3125421639",
"1293138521",
"2311944581"]
data_exo = utils.readfile("data/d15_v2.txt")
#print(data_exemple)
#print(data_exo)

def setor(tab, e, v = 1):
    if not e in tab.keys():
        tab[e] = 0
    tab[e]+=v
    return tab
    
def pf(k):
    #print(k)
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)


def process(data):
    mapc = {}
    maxi = len(data)
    maxj = len(data[0])
    for i,line in enumerate(data):
        for j, lett in enumerate(list(line)):
            l = int(lett)
            mapc[fp(i,j)] = l
            # v2
            for ii in range(0,5):
                for jj in range(0,5):
                    nlett = l + ii + jj
                    if nlett > 18:
                        nlett -= 18
                    if nlett > 9:
                        nlett -= 9
                    mapc[fp(i+ii*maxi,j+jj*maxj)]= nlett
    
    #return mapc,maxi,maxj
    #stri = ""
    #for j in range(0,maxj*5):
    #    for i in range(0,maxi*5):
    #        stri += str(mapc[fp(j,i)])
    #    print(stri)
    #    stri = ""
    #print(stri)
        
    return mapc,maxi*5,maxj*5

def ppath(datap):
    mapc,maxi,maxj = process(datap)
    lowpath = sum([int(x) for x in datap[0]]) + sum([int(x[-1]) for x in datap] )
    print("mi, mj =  ", maxi,".",maxj,"lowpath", lowpath)
    paths  = [
        ([fp(0,0)], 0)
    ]
    keep = True
    step = 0
    while keep:
        skip = 0
        skip2 = 0
        step += 1
        pathlist = []
        for (path, risk) in paths:
            i,j = pf(path[-1])
            #print("path",path,"i,j = ", i, ".", j)
            for (ni,nj) in [(i+1,j),(i,j+1), (i-1,j) ,(i,j-1)]:#
                if ni<maxi and nj<maxj and ni>=0 and nj>=0:
                    nkey = fp(ni,nj)
                    nrisk = risk+mapc[nkey]
                    if ni == maxi-1 and nj == maxj-1:
                        if nrisk < lowpath:
                            #print(">", path+[nkey], "nrisk", nrisk )
                            lowpath = nrisk
                        else:
                            skip += 1
                    if not nkey in path:
                        if nrisk + (maxi-ni) + (maxj-nj) <= lowpath:
                            pathlist.append( (path+[nkey], nrisk) )
                        else : 
                            skip2 += 1
        print( "step", step, " path:", lowpath, " len ", len(pathlist), "skip", skip, "skip2", skip2)
        paths = pathlist.copy()
        keep = len(pathlist) != 0

def djikstra(datap):
    mapc,maxi,maxj = process(datap)
    visiteddistance = {}
    distance = {}
    node = fp(0,0)
    distance[node] = 0
    keep = True
    while keep:
        i,j = pf(node)
        #keep = False
        for (ni,nj) in [(i+1,j),(i,j+1), (i-1,j) ,(i,j-1)]:
            if ni<maxi and nj<maxj and ni>=0 and nj>=0:
                nkey = fp(ni,nj)
                if not nkey in visiteddistance:
                    ndist = distance[node] + mapc[nkey]
                    if not nkey in distance or ndist < distance[nkey]:
                        distance[nkey] = ndist
        visiteddistance[node] = distance[node]
        if node == fp(maxi-1,maxj-1):
            return distance[node]
        del distance[node]
        tdist = -1
        tnode = 0
        for elnode,eldist in distance.items():
            if tdist == -1 or eldist < tdist:
                tdist = eldist
                tnode = elnode
        node = tnode
            
        
    #4 When we are done considering all of the unvisited neighbors of the current node, mark the current node as visited and remove it from the unvisited set. A visited node will never be checked again.
    #5 If the destination node has been marked visited (when planning a route between two specific nodes) or if the smallest tentative distance among the nodes i
    #n the unvisited set is infinity (when planning a complete traversal; occurs when there is no connection between the initial node and remaining unvisited nodes), then stop. The algorithm has finished.
    #6 Otherwise, select the unvisited node that is marked with the smallest tentative distance, set it as the new current node, and go back to step 3.

    # When planning a route, it is actually not necessary to wait until the destination node is "visited" as above: the algorithm can stop once the destination node 
    #has the smallest tentative distance among all "unvisited" nodes (and thus could be selected as the next "current"). 
    
pp = djikstra(data_exemple)
#ppath(data_exo)
print(pp)

p2 = djikstra(data_exo)
print(p2)
