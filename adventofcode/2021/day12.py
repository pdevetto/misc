import utils, sys
data_exemple = ["start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"]
data_exo = utils.readfile("data/d12.txt")
#print(data_exemple)
#print(data_exo)

def getgraph(rules):
    paths = {}
    for path in rules:
        [p1,p2] = path.split("-")
        if not p1 in paths.keys():
            paths[p1] = []
        if p2 != 'start' and p1 != 'end' and not p2 in paths[p1]:
            paths[p1].append(p2)
        if not p2 in paths.keys():
            paths[p2] = []
        if p1 != 'start' and p2 != 'end' and not p1 in paths[p2]:
            paths[p2].append(p1)
    return paths

def issmall(cave):
    return cave.lower() == cave

def ways(way, nodes):
    for node in nodes:            
        if issmall(node) and node in way and way[0] == 'start':
            yield ['0start'] + way[1:] + [node]
        if not issmall(node) or not node in way:
            yield way + [node]

def process(dataex):
    paths = getgraph(dataex)
    print(paths)
    theways = [["start"]]
    final_ways = []
    keep = True
    while keep:
    #for i in range(0,20):
        keep = False
        newways = theways.copy()
        theways = []
        #print("****************")
        for way in newways:
            last_r = way[-1]
            if last_r == "end":
                final_ways.append(way)
            else:
                keep = True
                if last_r in paths.keys():
                    dispo = list(set(paths[way[-1]]))
                else:
                    dispo = []
                #print("C : ", way, " => ", last_r, '  == ', '|'.join(dispo))
                if(len(dispo) != 0):
                    for nway in ways(way, dispo):
                        theways.append(nway)
                #print("-> ways")
                #print(theways)
    print("________________")
    print(final_ways)
    print(len(final_ways))
    
#process(data_exemple)
process(data_exo)
