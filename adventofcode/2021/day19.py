import json, re
from collections import Counter
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_exo = readfile("data/d19.txt")
data_exemple=["--- scanner 0 ---",
"0,2",
"4,1",
"3,3",
"",
"--- scanner 1 ---",
"-1,-1",
"-5,0",
"-2,1"]

#print(data_exemple)
#print(data_exo)

def process(data):
    scanners = {}
    current_scanner = -1
    for line in data:
        scanid = re.search('--- scanner ([0-9]*) ---', line)
        if scanid == None:
            if len(line) != 0:
                scanners[current_scanner].append( list(map(int, line.split(','))))
        else:
            current_scanner = int(scanid.group(1))
            scanners[current_scanner] = []
    return scanners
      
scanners = process(data_exemple)
#print(scanners)

#####################

def sort_beac(beacons, order=[[0,1],[1,1],[2,1]]):
    # sort list with key
    if len(order) == 1:
        beacons.sort(key=(lambda x: order[0][1]*x[order[0][0]]))
    if len(order) == 2:
        beacons.sort(key=(lambda x: 
                          order[0][1]*x[order[0][0]] * 1000 +
                          order[1][1]*x[order[1][0]]))
    if len(order) == 3:
        beacons.sort(key=(lambda x: 
                          order[0][1]*x[order[0][0]] * 1000000 +
                          order[1][1]*x[order[1][0]] * 1000 +
                          order[2][1]*x[order[2][0]]))
    #print(beacons)
    return beacons

assert sort_beac([[4,5,6],[1,6,2],[1,4,5]], [(0,1),(1,1),(2,1)]) == [[1,4,5],[1,6,2],[4,5,6]]
assert sort_beac([[4,5,6],[1,6,2],[1,4,5]], [(1,-1),(0,1),(2,1)]) == [[1,6,2],[4,5,6],[1,4,5]]

scanners_exemples = process(readfile("data/d19_exemple.txt"))
#print(scanners_exemples)

def get_composante(beacons, coord):
    c_b = list(map(lambda beacon: beacon[coord[0]], beacons)) 
    c_b = list(map(lambda x: x*coord[1], c_b))
    return c_b

def down_to_zero(listn, first= False):
    if first:
        mini = min(listn)-1
    else:
        positifs = list(filter(lambda  x: x>0, listn))
        if len(positifs) == 0:
            mini = 0
        else:
            mini = min(positifs)
    listn = list(map(lambda x: x-mini, listn))
    return listn, mini

if False:
    assert down_to_zero([-5,0,10], True) == ([1,6,16],-6)
    assert down_to_zero([-5,0,10]) == ([-15,-10,0],10)
    assert down_to_zero([27,50,98]) == ([0,23,71],27)
    assert down_to_zero([0,3,6,9,12], True) == ([1,4,7,10,13],-1)
    assert down_to_zero([0,3,6,9,12]) == ([-3,0,3,6,9],3)
    assert down_to_zero([1,9,10,11,19]) == ([0,8,9,10,18],1)

    aa = [684,325,127,1024,185,14541,14,1,-700]
    print(down_to_zero(aa))
    assert down_to_zero(aa) == (
                        [683,324,126,1023,184,14540,13,0,-701],1)

def commonlist(la,lb):
    ca = Counter(la)
    cb = Counter(lb)
    thecount = 0
    for e,count in ca.items():
        thecount += min(count,cb.get(e,0))
    return thecount
        
if False:
    assert commonlist([1,2,2,2,3,4,4,4],[]) == 0
    assert commonlist([1,2,3],[1,5,7]) == 1
    assert commonlist([1,1,2],[1,5]) == 1
    assert commonlist([1,1,2],[1,1,1,5]) == 2
    assert commonlist([1,1,2,2,3,4],[1,2,3,4]) == 4
    assert commonlist([1,1,2,2,3,4],[1,2,3,4,0]) == 4


    
def aligner_liste(lisa, lisb):
    lisa,smina = down_to_zero(lisa, True)
    lisb,sminb = down_to_zero(lisb, True)
    fmina = 0
    while max(lisa) > 0:
        lisa,mina = down_to_zero(lisa)
        fmina += mina
        newlisb = lisb.copy()
        fminb = 0
        while max(newlisb)> 0:
            newlisb, minb = down_to_zero(newlisb)
            fminb += minb
            cli = commonlist(lisa,newlisb)
            if cli>=12:
                delta = (smina + fmina) - (sminb + fminb)
                print(f"=> {cli} with {delta} ppp {smina} {fmina}")
                return True, delta
    return False, None

if True:
    assert aligner_liste([1,2,3, 4,5,6,  7,8,9,    10,11,12],
                         [5,6,7, 8,9,10, 11,12,13, 14,15,16])[0] == True

    b0 = [-618,-537,-447,404,544,528,-661,390,423,-345,459,-485]
    #assert aligner_liste(b0, [686,605,515,-336,-476,-460,729,-322,-355,413,-391,553]) == False
    #assert aligner_liste(b0, [422,423,917,658,619,603,430,571,545,935,539,889]) == False
    #assert aligner_liste(b0, [578,415,-361,858,847,-452,532,750,-477,-424,-444,-390]) == False
    #assert aligner_liste(b0, [-686,-605,-515,336,476,460,-729,322,355,-413,391,-553]) == True
    #assert aligner_liste(b0, [-422,-423,-917,-658,-619,-603,-430,-571,-545,-935,-539,-889]) == False
    #assert aligner_liste(b0, [578,-415,361,-858,-847,452,-532,-750,477,424,444,390]) == False
    assert aligner_liste(
        [-618,-537,-447,404,544,528,-661,390,423,-345,459,-485,100,-200,541],
        [-686,-605,-515,336,476,460,-729,322,355,-413,391,-553,1022,350]
    )[0] == True
    assert aligner_liste(
        [-618,-537,-447,404,544,528,-661,390,423,-345,459,-485,100,-200,541],
        [-686,-605,-515,336,476,460,-729,322,355,-413,391,-553,1022,350]
    )[0] == True

    
def test_beacon(sc_beac_1, sc_beac_2):
    all_orders = [
        [0,1], [0,-1],
        [1,1], [1,-1],
        [2,1], [2,-1]
    ]
    bigdelta = []
    #print(sc_beac_1)
    compo_b1 = [
        get_composante(sc_beac_1, [0,1]),
        get_composante(sc_beac_1, [1,1]),
        get_composante(sc_beac_1, [2,1])
    ]
    for i,composante in enumerate(compo_b1):
        print(f"COMPO {i}")
        foundit = False
        for order in all_orders:
            compo_b2 = get_composante(sc_beac_2, order)
            align, delta = aligner_liste(composante, compo_b2)
            if align:
                foundit = True
                bigdelta.append(order + [delta])
                all_orders = [o for o in all_orders if o[0] != order[0]]
        if not foundit:
            return []
    return bigdelta

def applybeacon(beacons, bd):
    newbeacons = []
    for beacon in beacons:
        #[[0, -1, 68], [1, 1, -1246], [2, -1, -43]]
        newbeacons.append([
            (beacon[bd[i][0]] * bd[i][1]) + bd[i][2] for i in range(0,3)
        ])
    return newbeacons

def process_scanners(scans):
    scanid = []
    allbeacons = [beacon for beacon in scans[0]]
    okscnners = [0]
    for i in range(0,20):
        print(f"SCAAA : {len(okscnners)} for {len(scans)}")
        if len(okscnners) == len(scans):
            return scanid
        i += 0
        for j,next_scan in scans.items():
            if not j in okscnners:
                print(f"[[[[ test beacon {j}")
                res = test_beacon(allbeacons, next_scan)
                if len(res) != 0:
                    okscnners.append(j)
                    scanid.append([res[i][2] for i in range(0,3)])
                    newbeacons = applybeacon(next_scan, res)
                    #print(newbeacons)
                    allbeacons = list({f"{b[0]}.{b[1]}.{b[2]}":b for b in allbeacons + newbeacons}.values())
    
scanid = process_scanners(scanners_exemples)
print(scanid)

scanners_ex0 = process(readfile("data/d19.txt"))
scanid = process_scanners(scanners_ex0)
print("Finish")
print(scanid)

maxdist = 0
for i,b in enumerate(scanid):
    for j,b2 in enumerate(scanid[i+1:]):
        #print (b, b2)
        ss = sum( [ abs(b2[x]-b[x]) for x in range(0,3)] )
        #print (ss)
        if ss > maxdist:
            maxdist = ss

print("max", maxdist)
        

