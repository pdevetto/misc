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

def getmap(mapw, x, y):
    coord = fp(x,y)
    if not coord in mapw.keys():
        return "."
    return mapw[coord]
        
data_ex = [
    "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
    "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
    "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
    "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
    "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
    "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
    "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
    "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
    "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
    "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
    "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
    "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
    "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
    "Sensor at x=20, y=1: closest beacon is at x=15, y=3"
]
data = readfile("d15.txt")

def manhattan(a,b,x,y):
    return abs(a-x) + abs(b-y)

def not_kevin_beacon(mapb, sensor, beacon, nline):
    manh = manhattan(sensor[0],sensor[1],beacon[0],beacon[1])
    if (sensor[1] > nline and nline > sensor[1] - manh) or (sensor[1] < nline and nline < sensor[1] + manh):
        largline = manh - abs(sensor[1]-nline)
        for i in range(0,largline+1):
            if getmap(mapb, sensor[0]+i, nline) == ".":
                mapb[fp(sensor[0]+i, nline)] = "#"
            if getmap(mapb, sensor[0]-i, nline) == ".":
                mapb[fp(sensor[0]-i, nline)] = "#"
    return mapb
        
def d151(data, nline):
    mapb = {}
    ite = 1
    for line in data:
        print("iteration", ite)
        ite += 1
        regexp = r"Sensor at x=([-0-9]*), y=([-0-9]*): closest beacon is at x=([-0-9]*), y=([-0-9]*)"
        [(xs,ys,xb,yb)] = re.findall(regexp, line)
        sensor,beacon= (int(xs),int(ys)),(int(xb),int(yb))
        if sensor[1] == nline:
            mapb[fp(sensor[0], sensor[1])]="S"
        if beacon[1] == nline:
            mapb[fp(beacon[0], beacon[1])]="B"
        print(len(mapb))
        mapb = not_kevin_beacon(mapb, sensor, beacon, nline)
    #print_map(mapb)
    print(len([val for coo,val in mapb.items() if pf(coo)[1] == nline and val == "#"]))

#d151(data_ex, nline = 10)


start_time = time.time()
#d151(data, nline = 2000000)
print("--- %s seconds ---" % (time.time() - start_time))

def d152(data, maxc):
    sensors={}
    beacons={}
    for line in data:
        regexp = r"Sensor at x=([-0-9]*), y=([-0-9]*): closest beacon is at x=([-0-9]*), y=([-0-9]*)"
        [(xs,ys,xb,yb)] = re.findall(regexp, line)
        sensor,beacon= (int(xs),int(ys)),(int(xb),int(yb))
        sensors[fp(sensor[0], sensor[1])] = (
            sensor[0], sensor[1],manhattan(sensor[0],sensor[1],beacon[0],beacon[1]))
        beacons[fp(beacon[0], beacon[1])] = 1

    count = 0
    for x in range(0,maxc+1):
        if x%100000 == 0:
            print("x:", x)
        y = 0
        while y<maxc:
            nomatch = 0
            for ssi,ss in sensors.items():
                if manhattan(ss[0],ss[1],x,y) <= ss[2]:
                    nomatch += 1
                    if y < ss[1]:
                        y += (ss[1] - y) * 2
                    else:
                        y += ss[2] - abs( x - ss[0] )  - (y-ss[1])
            if nomatch == 0:
                print(" NOPPPPPPPP ", x, y)
                if fp(x,y) not in beacons.keys():
                    if fp(x,y) not in sensors.keys():
                        print("OOOOOOK")
                        yield (x,y)
            y+=1

assert manhattan(8,7,14,4) == 9
for (a,b) in d152(data_ex, maxc = 20):
    assert (a,b) == (14,11)

print("start")
start_time = time.time()
for (a,b) in d152(data, maxc = 4000000):
    print(a * 4000000 + b)
    
print("--- %s seconds ---" % (time.time() - start_time))

#a = 2978645 
#b = 3249288
