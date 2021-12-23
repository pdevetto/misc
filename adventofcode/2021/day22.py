import json, re
from collections import Counter
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

def procedure(data):
    engine = {}
    for line in data:
        group = re.match('(on|off) x=([\-0-9]*)..([\-0-9]*),y=([\-0-9]*)..([\-0-9]*),z=([\-0-9]*)..([\-0-9]*)', line)
        if group != None:
            st = group[1] == 'on'
            x1,y1,z1=max(-50,int(group[2])),max(-50,int(group[4])),max(-50,int(group[6]))
            x2,y2,z2=min( 50,int(group[3])),min( 50,int(group[5])),min( 50,int(group[7]))
            for x in range(x1,x2+1):
                for y in range(y1,y2+1):
                    for z in range(z1,z2+1):
                        k = fp(x,y,z)
                        if st:
                            engine[k] = True
                        else:
                            if engine.get(k,False):
                                del engine[k]
    return engine

def overlap_comp(n1,n2,m1,m2):
    b1,b2 = 0,0
    if m2 < n1 or m1 > n2:
        return False
    if m1 < n1:
        b1 = n1
    else: 
        b1 = m1
    if m2 > n2:
        b2 = n2
    else:
        b2 = m2
    return (b1,b2)

assert overlap_comp(0,10,-5,15) == (0,10)
assert overlap_comp(0,10,-5,10) == (0,10)
assert overlap_comp(0,10,-5,4) == (0,4)
assert overlap_comp(0,10,2,3) == (2,3)
assert overlap_comp(0,10,10,20) == (10,10)
assert overlap_comp(0,10,5,15) == (5,10)
assert overlap_comp(0,10,15,20) == False

def overlap_diff(n1,n2,m1,m2):
    comp = []
    b1,b2 = 0,0
    if m2 < n1 or m1 > n2:
        comp = [(n1,n2)]
    else:
        if n1 < m1:
            comp.append((n1,m1-1))
        else: 
            b1 = m1
        if m2 < n2:
            comp.append((m2+1,n2))
        else:
            b2 = m2
    #print("compared", n1,n2,m1,m2, " >> ", comp)
    return comp

assert overlap_diff(-5,15,0,10) == [(-5,-1),(11,15)]
assert overlap_diff(-5,10,0,10) == [(-5,-1)]
assert overlap_diff(-5,4,0,10) == [(-5,-1)]
assert overlap_diff(2,3,0,10) == []
assert overlap_diff(0,10,2,3) == [(0,1),(4,10)]
assert overlap_diff(0,10,10,20) == [(0,9)]
assert overlap_diff(10,20,0,10) == [(11,20)]
assert overlap_diff(5,15,0,10) == [(11,15)]
assert overlap_diff(15,20,0,10) == [(15,20)]
assert overlap_diff(0,6,2,4) == [(0,1),(5,6)]

def testproxi(cub1,cub2):
    if cub1 == cub2:
        return cub1
    for [(a,b),(c,d),(e,f)] in [[(0,1),(2,3),(4,5)],[(0,1),(4,5),(2,3)],[(2,3),(4,5),(0,1)]]:
        if cub1[a:b+1] == cub2[a:b+1] and cub1[c:d+1] == cub2[c:d+1]:
            cub = [0,0,0,0,0,0]
            cub[a] = cub1[a]
            cub[b] = cub1[b]
            cub[c] = cub1[c]
            cub[d] = cub1[d]
            #if cub2[e] < cub1[e] and cub1[e] < cub2[f]:
            #    cub[e] = cub1[e]
            #    cub[f] = max(cub1[f],cub2[f])
            #    return cub
            #if cub1[e] < cub2[e] and cub1[e] < cub2[f]:
            #    cub[e] = cub1[e]
            #    cub[f] = max(cub1[f],cub2[f])
            #    return cub
            
            if cub1[f]+1 == cub2[e] or cub1[f] == cub2[e]:
                cub[e] = cub1[e]
                cub[f] = cub2[f]
                return cub
            if cub2[f]+1 == cub1[e] or cub2[f] == cub1[e]:
                cub[e] = cub2[e]
                cub[f] = cub1[f]
                return cub
    return False

if False:
    assert testproxi([0,6,0,6,0,6], [6,7,0,6,0,6]) == [0,7,0,6,0,6]
    assert testproxi([0,6,0,6,0,6], [0,6,0,6,7,7]) == [0,6,0,6,0,7]
    tp = testproxi([4,10,0,2,0,3], [0,3,0,3,0,3])
    print(tp)
    assert tp == False

def reduce(cubes):
    #print("REDUCE", len(cubes))
    allcubes = cubes
    endcubes = []
    while len(allcubes)!=0:
        nextcubes = []
        cub0=allcubes[0]
        allcubes=allcubes[1:]
        while len(allcubes) != 0:
            cubn=allcubes[0]
            allcubes=allcubes[1:]
            crush_cub = testproxi(cub0,cubn)
            if crush_cub != False:
                #print("crush ", cub0, cubn, " => ", crush_cub)
                cub0 = crush_cub
            else:
                nextcubes.append(cubn)
        endcubes.append(cub0)
        allcubes = nextcubes.copy()
    #print(len(endcubes), endcubes)
    return endcubes

assert reduce([[0,3,0,2,0,3], [0,3,3,3,0,3], [4,10,0,2,0,3]]) == [[0,3,0,3,0,3],[4,10,0,2,0,3]] 
assert reduce([[-20,34,-40,-6,44,-1],[10,12,23,45,60,80]]) == [[-20,34,-40,-6,44,-1],[10,12,23,45,60,80]]

def is_overlap(zone1,zone2):
    ov_cp = {}
    for c,(i,j) in {'x':(0,1),'y':(2,3),'z':(4,5)}.items():
        ov_cp[c] = overlap_comp( zone1[i],zone1[j],zone2[i],zone2[j] )
        if ov_cp[c] == False:
            return False
    else:
        return True

assert is_overlap([0,3,0,2,0,3], [0,3,3,3,0,3]) == False
assert is_overlap([0,3,0,3,0,3], [0,3,3,3,0,3]) == True
assert is_overlap([-20,34,-40,-6,44,-1],[10,12,23,45,60,80]) == False

def overlap(zone1, zone2, on=True):
    ov_cp = {}
    ov_df = {}
    ov_df_neg = {}
    for c,(i,j) in {'x':(0,1),'y':(2,3),'z':(4,5)}.items():
        ov_cp[c] = overlap_comp( zone1[i],zone1[j],zone2[i],zone2[j] )
        ov_df[c] = overlap_diff( zone1[i],zone1[j],zone2[i],zone2[j] )
        ov_df_neg[c] = overlap_diff( zone2[i],zone2[j],zone1[i],zone1[j] )
        if ov_cp[c] == False:
            return [zone1]
    finalcube = []
    if on:
        if len(ov_df['x'])+len(ov_df['y'])+len(ov_df['z']) == 0:
            return []
        coordA = {}
        for coo in ['x','y','z']:
            coordA[coo]=([ov_cp[coo]]+ov_df[coo])
            if [] in coordA[coo]:
                coordA[coo].remove([])
        for (oox1,oox2) in coordA['x']:
            for (ooy1,ooy2) in coordA['y']:
                for (ooz1,ooz2) in coordA['z']:
                    kub = [oox1,oox2,ooy1,ooy2,ooz1,ooz2]
                    if not is_overlap(kub,[ov_cp['x'][0],ov_cp['x'][1],ov_cp['y'][0],
                               ov_cp['y'][1],ov_cp['z'][0],ov_cp['z'][1]]) and not is_overlap(kub,zone2):
                        finalcube.append(kub)
    else:
        if len(ov_df['x'])+len(ov_df['y'])+len(ov_df['z']) == 0:
            return []
        #if len(ov_df_neg['x'])+len(ov_df_neg['y'])+len(ov_df_neg['z']) == 0:
        #    return [zone1]
        coordss = {}
        for coo in ['x','y','z']:
            coordss[coo]=([ov_cp[coo]]+ov_df[coo])
            if [] in coordss[coo]:
                coordss[coo].remove([])
        for (oox1,oox2) in coordss['x']:
            for (ooy1,ooy2) in coordss['y']:
                for (ooz1,ooz2) in coordss['z']:
                    kub = [oox1,oox2,ooy1,ooy2,ooz1,ooz2]
                    if not is_overlap(kub,[ov_cp['x'][0],ov_cp['x'][1],ov_cp['y'][0],
                               ov_cp['y'][1],ov_cp['z'][0],ov_cp['z'][1]]) and not is_overlap(kub,zone2):
                        finalcube.append(kub)
    if False:
        print("CP:",ov_cp)
        print("DF:",ov_df)
        print("NG:",ov_df_neg)
        print(" >:",finalcube)
    finalcube = reduce(finalcube)        
    return finalcube

def compt(zones):
    comptage = 0
    for zone in zones:
        comptage += (+1+abs(zone[1]-zone[0])) * (+1+abs(zone[3]-zone[2])) * (+1+abs(zone[5]-zone[4]))
    return comptage        

assert overlap([0,10,0,10,0,10], [11,20,11,20,11,20]) == [[0,10,0,10,0,10]]
assert overlap([0,10,0,10,0,10], [0,5,0,5,0,5], True) == [[0, 5, 0, 10, 6, 10], [0, 10, 6, 10, 0, 5], [6, 10, 0, 5, 0, 10], [6, 10, 6, 10, 6, 10]]
assert overlap([0,10,0,10,0,10], [20,25,20,25,20,25], False) == [[0,10,0,10,0,10]]
base = [(0,1),(2,4),(5,6)]
result = [ [x1,x2,y1,y2,z1,z2] for (x1,x2) in base for (y1,y2) in base for (z1,z2) in base
         if [x1,x2,y1,y2,z1,z2] != [2,4,2,4,2,4]]
realresult = overlap([0,6,0,6,0,6], [2,4,2,4,2,4], False)
assert compt(result) == 316
assert compt(realresult) == 316
assert overlap([0,6,0,6,0,6], [6,7,0,6,0,6], False) == [[0, 5, 0, 6, 0, 6]]
assert overlap([0,3,0,3,0,3], [0,10,0,2,0,3], True) == [[0, 3, 3, 3, 0, 3]]
assert overlap([0,3,0,3,0,3], [0,10,0,4,0,3], True) == []
assert overlap([0,3,0,3,0,3], [1,10,0,4,0,3], True) == [[0,0,0,3,0,3]]

newtestres = overlap([-20, 26, -36, 17, -47, -27],[-22, 28, -29, 23, -38, 16], True)
assert newtestres == [[-20, 26, -36, 17, -47, -39], [-20, 26, -36, -30, -38, -27]]

assert overlap([-20, 26, -36, 17, -47, -27],[-20, 26, -36, 17, -47, -39], True) == [[-20, 26, -36, 17, -38, -27]]
assert overlap([-20, 26, -36, 17, -47, -27],[-20, 26, -36, -30, -38, -27], True) == [[-20, 26, -36, 17, -47, -39], [-20, 26, -29, 17, -38, -27]]

nres = overlap([0,6,0,6,0,6], [6,9,2,4,2,4], True)
assert compt(nres) == 334

def procedure2(data):
    zones = []
    step = 0
    comptage = 0
    for line in data:
        step += 1
        group = re.match('(on|off) x=([\-0-9]*)..([\-0-9]*),y=([\-0-9]*)..([\-0-9]*),z=([\-0-9]*)..([\-0-9]*)', line)
        if group != None:
            st = (group[1] == 'on')
            #x1,y1,z1=max(-50,min(50,int(group[2]))),max(-50,min(50,int(group[4]))),max(-50,min(50,int(group[6])))
            #x2,y2,z2=max(-50,min(50,int(group[3]))),max(-50,min(50,int(group[5]))),max(-50,min(50,int(group[7])))
            x1,y1,z1=int(group[2]),int(group[4]),int(group[6])
            x2,y2,z2=int(group[3]),int(group[5]),int(group[7])
            temp_zone = [x1,x2,y1,y2,z1,z2]
            new_zones = []
            for zone in zones:
                if not is_overlap(zone,temp_zone):
                    new_zones.append(zone)
                else:
                    ozone = overlap(zone, temp_zone, on=st)
                    for nzone in ozone:
                        if not is_overlap(nzone,temp_zone):
                            new_zones.append(nzone)
            if st:
                new_zones.append(temp_zone)
            #lz = len(new_zones)
            print("[",step,"] ") #,lz)
            #zones = reduce(new_zones.copy())
            #zones = reduce(new_zones.copy())
            zones = new_zones
            #print("FINAL ZONE :: ", zones, " = ", compt(zones))
            
    #print("final  : ZON ", len(zones))
    print("count", compt(zones))
    return zones
        
            
data_test0 = ["on x=10..12,y=10..12,z=10..12",
"on x=11..13,y=11..13,z=11..13",
"off x=9..11,y=9..11,z=9..11",
"on x=10..10,y=10..10,z=10..10"]

data_test = ["on x=-20..26,y=-36..17,z=-47..7",
"on x=-20..33,y=-21..23,z=-26..28",
"on x=-22..28,y=-29..23,z=-38..16",
"on x=-46..7,y=-6..46,z=-50..-1",
"on x=-49..1,y=-3..46,z=-24..28",
"on x=2..47,y=-22..22,z=-23..27",
"on x=-27..23,y=-28..26,z=-21..29",
"on x=-39..5,y=-6..47,z=-3..44",
"on x=-30..21,y=-8..43,z=-13..34",
"on x=-22..26,y=-27..20,z=-29..19",
"off x=-48..-32,y=26..41,z=-47..-37",
"on x=-12..35,y=6..50,z=-50..-2",
"off x=-48..-32,y=-32..-16,z=-15..-5",
"on x=-18..26,y=-33..15,z=-7..46",
"off x=-40..-22,y=-38..-28,z=23..41",
"on x=-16..35,y=-41..10,z=-47..6",
"off x=-32..-23,y=11..30,z=-14..3",
"on x=-49..-5,y=-3..45,z=-29..18",
"off x=18..30,y=-20..-8,z=-3..13",
"on x=-41..9,y=-7..43,z=-33..15",
"on x=-54112..-39298,y=-85059..-49293,z=-27449..7877",
"on x=967..23432,y=45373..81175,z=27513..53682"]
   
data_exo = readfile("data/d22.txt")
data_exemple = readfile("data/d22_exemple.txt")

print("Node OK")
#zones = procedure2(data_test)
#zones = procedure2(data_test0)
#zones = procedure2(data_exemple)
from datetime import datetime
a = datetime.now().strftime("%H:%M:%S")
zones = procedure2(data_exo)
b = datetime.now().strftime("%H:%M:%S")
print(a)
print(b)
