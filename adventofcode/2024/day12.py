import utils, re
import itertools

data_ex = [
    "RRRRIICCFF",
    "RRRRIICCCF",
    "VVRRRCCFFF",
    "VVRCCCJFFF",
    "VVVVCJJCFE",
    "VVIVCCJJEE",
    "VVIIICJJEE",
    "MIIIIIJJEE",
    "MIIISIJEEE",
    "MMMISSJEEE",
]
data_ex2 = [
    "AAAA",
    "BBCD",
    "BBCC",
    "EEEC",
]
data = utils.readfile("data/day12.txt")

def get_map(data):
    mapland = {}
    for i, line in enumerate(data):
        for j, field in enumerate(line):
            k = utils.xy2k(i, j)
            mapland[k] = field
    return mapland

def find_field(k, mapland):
    perimeter = 0
    field = mapland.get(k)
    explore = [k]
    fields = []
    edges = []
    ref_ed = {
        "-1.0":((0,0),(0,1)),
        "0.-1":((1,0),(0,0)),
        "1.0":((1,1),(1,0)),
        "0.1":((0,1),(1,1)),
    }
    while len(explore) > 0:
        k = explore.pop()
        fields.append(k)
        for delta in [(0,1),(1,0), (0,-1),(-1,0)]:
            dk = utils.k_delta(k, delta)
            if mapland.get(dk) == field:
                if not dk in fields and not dk in explore:
                    explore.append(dk)
            else:
                ref_edge = ref_ed.get( utils.xy2k( delta[0], delta[1] ) )
                edges.append( (utils.k_delta(k, ref_edge[0]), utils.k_delta(k,ref_edge[1]) ))
                perimeter += 1
    #print("field ", field, " len=",len(fields), " peri=", perimeter, "   ", fields)
    return len(fields), perimeter, fields, edges

assert find_field('0.0', get_map(data_ex2))[0:2] == (4, 10)
assert find_field('1.0', get_map(data_ex2))[0:2] == (4, 8)
assert find_field('1.2', get_map(data_ex2))[0:2] == (4, 10)
assert find_field('1.3', get_map(data_ex2))[0:2] == (1, 4)
assert find_field('3.0', get_map(data_ex2))[0:2] == (3, 8)

#print( find_field('3.0', get_map(data_ex2))[2] )
#print( find_field('3.0', get_map(data_ex2))[3] )

def align(v1, v2):
    x1,y1 = utils.k2xy(v1[0])
    x2,y2 = utils.k2xy(v1[1])
    a1,b1 = utils.k2xy(v2[0])
    a2,b2 = utils.k2xy(v2[1])
    if x1 == x2 == a1 == a2 and y1 != y2 and b1 != b2:
        if y1 == b2:
            return (utils.xy2k(x1,b1), utils.xy2k(x1,y2))
        if b1 == y2: 
            return (utils.xy2k(x1,y1), utils.xy2k(x1,b2))
    if y1 == y2 == b1 == b2:
        if x1 == a2:
            return (utils.xy2k(a1,b1), utils.xy2k(x2,b1))
        if a1 == x2: 
            return (utils.xy2k(x1,b1), utils.xy2k(a2,b1))
    return None

assert align(('3.1', '4.1'), ('4.1', '5.1')) == ('3.1', '5.1')
assert align(('4.1', '5.1'), ('3.1', '4.1')) == ('3.1', '5.1')
assert align(('3.1', '4.1'), ('5.1', '4.1')) == None
assert align(('4.1', '3.1'), ('5.1', '4.1')) == ('5.1', '3.1')
assert align(('3.1', '4.1'), ('4.1', '8.1')) == ('3.1', '8.1')
print( align(('0.1', '0.2'), ('0.2', '0.3')) )
assert align(('0.1', '0.2'), ('0.2', '0.3')) == ('0.1', '0.3')
assert align(('0.1', '0.2'), ('0.3', '0.8')) == None
assert align(('3.1', '4.1'), ('4.1', '4.2')) == None

def reduce_edges(edges):
    print("Given edges :", edges)
    new_edges = []
    merged = False
    keep = True
    while keep and len(edges)>0:
        edgeA = edges.pop()
        merged = False
        for edgeB in edges:
            edgeAB = align(edgeA, edgeB)
            if edgeAB and not merged:
                edges.append( edgeAB )
                edges.remove(edgeB)
                merged = True
                break
        if not merged:
            new_edges.append(edgeA)
    #print("newed = ", new_edges)
    #print("edges = ", edges)
    lesedges = new_edges + edges
    print("-- les edges ", lesedges)
    return sorted(lesedges)

print(find_field('1.3', get_map(data_ex2))[3])
assert find_field('1.3', get_map(data_ex2))[3] == [('1.4', '2.4'), ('2.4', '2.3'), ('2.3', '1.3'), ('1.3', '1.4')]
print(find_field('3.0', get_map(data_ex2))[3])
assert find_field('3.0', get_map(data_ex2))[3] == [('4.1', '4.0'), ('4.0', '3.0'), ('3.0', '3.1'), ('4.2', '4.1'), ('3.1', '3.2'), ('3.3', '4.3'), ('4.3', '4.2'), ('3.2', '3.3')]

#assert reduce_edges( [('3.1', '4.1'), ('4.1', '5.1')] ) == [('3.1', '5.1')]
assert reduce_edges( 
    [('4.1', '4.0'), ('4.0', '3.0'), ('3.0', '3.1'), ('4.2', '4.1'), ('3.1', '3.2'), ('3.3', '4.3'), ('4.3', '4.2'), ('3.2', '3.3')] 
) == sorted([('3.0', '3.3'), ('4.3', '4.0'), ('3.3', '4.3'), ('4.0', '3.0')])
assert reduce_edges( [('2.3', '2.4'), ('1.4', '2.4'), ('1.3', '2.3'), ('1.3', '1.4')] ) == sorted([('2.3', '2.4'), ('1.4', '2.4'), ('1.3', '2.3'), ('1.3', '1.4')])

def day12(data):
    mapland = get_map(data)
    fields = {}
    sumfield = 0
    sumedges = 0
    for k, field in mapland.items():
        if not k in fields.get(field, []):
            print("Field ", k, " is ", field)
            fs, peri, thefield, edges = find_field(k, mapland)
            sumfield += peri * fs
            nbedges = len(reduce_edges(edges))
            sumedges += nbedges * fs
            fields[field] = fields.get(field, []) + thefield
            print(peri * fs, "\t E:", nbedges, fs, " \t = ", nbedges * fs)
    print(sumfield, sumedges)
    return sumfield, sumedges
        
assert (day12(data_ex2)) == (140, 80)
print("-" * 30)
assert (day12(data_ex)) == (1930, 1206)
print("Go day 12")

ex3 = ["EEEEE","EXXXX","EEEEE","EXXXX","EEEEE"]
assert (day12(ex3))[1] == 236
ex4 = [
"AAAAAA",
"AAABBA",
"AAABBA",
"ABBAAA",
"ABBAAA",
"AAAAAA",
]
print ("*" *50)
assert (day12(ex4))[1] == 368
print(day12(data))
