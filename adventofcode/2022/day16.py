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
    "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
    "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
    "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
    "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
    "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
    "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
    "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
    "Valve HH has flow rate=22; tunnel leads to valve GG",
    "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
    "Valve JJ has flow rate=21; tunnel leads to valve II"
]
data = readfile("d16.txt")

def redundant(string):
    string = "".join([lett for lett in string.split(".")])
    for i in range(0,len(string)):
        for j in range(i+2, i+(len(string)-i)//2+1):
            if string[i:j]+string[i:j] in string:
                return True
    return False
        
    
assert redundant("AA.AA") == True
assert redundant("BB.AA.AA") == True
assert redundant("AA.BB") == False
assert redundant("AA.BB.CC.AA.BB") == False
assert redundant("AA.BB.AA.BB.CC") == True
assert redundant("AA.BB.CC.AA.BB.DD") == False
assert redundant("AA.BB.CC.AA.BB.CC.EE") == True


def oh_djidji(graph, rate):
    print(graph, rate)
    paths = {"AA":([],0)}
    for i in range(1,30):
        print("Minute", i, "sizepaths", len(paths))
        newpaths = {}    
        for path, (valvs,press) in paths.items():
            curpress = sum([rat for valv,rat in rate.items() if valv in valvs])
            nodes = path.split(".")
            cur = nodes[-1]
            if len(valvs) != len(rate):
                if not cur in valvs:
                    newpaths[path] = (valvs + [cur], press+curpress)
                for node in graph[cur]:
                    if not redundant(path+"."+node):
                        newpaths[path+"."+node] = (valvs, press+curpress)
            else:
                newpaths[path] = (valvs, press+curpress)
        
        presses = list(set([press for path, (valvs,press) in newpaths.items()]))
        presses.sort()
        paths = {path: (valvs,press) for path, (valvs,press) in newpaths.items() if press in presses[-1:]}[100]
            
    minscore = 0
    for path, (valvs, press) in paths.items():
        print(path, press)
    print(max( [press for path, (valvs, press) in paths.items()]))

def d161(data):
    graph = {}
    rate = {}
    for line in data:
        regexp = r"^Valve ([A-Z]*) has flow rate=([0-9]*); tunnels? leads? to valves? ([A-Z, ]*)$"
        results = re.findall(regexp, line)
        print(results)
        if results:
            rs = results[0]
            graph[rs[0]] = [node.strip() for node in rs[2].split(",")]
            rate[rs[0]] = int(rs[1])
    oh_djidji(graph, rate)
    
        
        
d161(data_ex)

start_time = time.time()
#d161(data)
print("--- %s seconds ---" % (time.time() - start_time))
