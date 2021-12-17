import utils, sys
data_exemple = ["2199943210","3987894921","9856789892","8767896789","9899965678"]
data_exo = utils.readfile("data/d09.txt")
print(data_exemple)
#print(data_exo)

def getmap(highs):
    maphigh = {}
    for i,highline in enumerate(highs):
        for j,high in enumerate([x for x in highline]):
            maphigh[fp(i,j)] = int(high)
    return maphigh

def getlowpt(maph):
    lowp = 0
    risk = 0
    basinsize = []
    for key in maph.keys():
        i,j = pf(key)
        low = True
        for nkey in [fp(i-1, j),fp(i+1, j),fp(i, j-1),fp(i, j+1)]:
            if nkey in maph:
                low = low and (maph[nkey] > maph[key])
        if low: 
            lowp += 1
            risk += 1 + maph[key]
            #print("lowp ", i,",",j, " v", maph[key])
            basinsize.append(findbasin(i,j,maph))
    print("risk", risk, "lowp", lowp)
    return basinsize
    
def pf(k):
    [i,j] = k.split('.')
    return int(i), int(j)
def fp(i,j):
    return str(i) + '.' + str(j)

bigall = []

def findbasin(i,j,maph):
    keep = True
    allpoints = []
    newpoints = [fp(i,j)]
    base = maph[fp(i,j)]
    print ("findbasin: ", i,",",j, " => ", base)
    while base != 9 and len(newpoints)!= 0:
        allpoints = list(set(allpoints)) + list(set(newpoints))
        points = list(set(newpoints.copy()))
        newpoints = []
        for k in points:
            i,j = pf(k)
            for nkey in [fp(i-1, j),fp(i+1, j),fp(i, j-1),fp(i, j+1)]:
                if nkey in maph and maph[nkey] > maph[k] and maph[nkey]!= 9 and not nkey in bigall:
                    newpoints.append(nkey)
                    bigall.append(nkey)
                        
        print("base : ", base, "point", points)
        base += 1
    print("NEW basin", allpoints, "size", len(allpoints))
    return len(allpoints)
                    
            
        
        
    
mh = getmap(data_exo)
#print(mh)
sizes = getlowpt(mh)
#print(sizes)

sizes.sort()
print(sizes)
        
        