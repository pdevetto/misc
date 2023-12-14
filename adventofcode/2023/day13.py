import sys, re, time, numpy, collections, numpy

def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_ex= [
    "#.##..##.",
    "..#.##.#.",
    "##......#1",
    "##......#",
    "..#.##.#.",
    "..##..##.",
    "#.#.##.#.",
    "",
    "#...##..#",
    "#....#..#",
    "..##..###",
    "#####.##.",
    "#####.##.",
    "..##..###",
    "#....#..#"
]
data = readfile("data/d_2023_13.txt")

def ij(i, j):
    return str(i)+"."+str(j)

def find_center(s):
    possibles = []
    s= ''.join(map(str, s))
    for i in range(1,len(s)):
        left = s[0:i][::-1]
        right_r = s[i:]
        if (left == right_r[0:len(left)]
            or left[0:len(right_r)] == right_r ):
            possibles.append( i )
    return set(possibles)

assert find_center([0,1,2,2,1,0,0,1,2,2]) == {3, 6, 9}
assert find_center([0,1,2,2]) == {3}
assert find_center([0,1,2,2,1,0]) == {3}


assert find_center("012210") == {3}
assert find_center("0122") == {3}
assert find_center("01221089A") == {3}


def detect_mirror(mapp, max_i, max_j):
    print("/" * 20, "\n", "/" * 20, f"\n {max_i} {max_j}")
    mirr_rows = {}
    from_row = True
    mirr_cols = {}
    from_col = True
    for step in range(1, max(max_i, max_j)+1):
        print("Step", step)
        if from_col and step <= max_j:
            cols = [mapp[ij(i,step)] for i in range(1,max_i+1)]
            if step == 1: 
                mirr_cols = find_center(cols)
            else:
                mirr_cols = mirr_cols.intersection(find_center(cols))
            if len(mirr_cols) == 0:
                from_col = False
        if from_row and step <= max_i:
            rows = [mapp[ij(step,j)] for j in range(1,max_j+1)]
            if step == 1:
                mirr_rows = find_center(rows)
            else:
                mirr_rows = mirr_rows.intersection(find_center(rows))
            if len(mirr_rows) == 0:
                from_row = False
        print( "Mirrors", mirr_cols, " col - rows ", mirr_rows)
    if len(mirr_rows) == 1 and len(mirr_cols) == 0:
        return list(mirr_rows)[0]
    if len(mirr_cols) == 1 and len(mirr_rows) == 0:
        return list(mirr_cols)[0] * 100
    raise Exception("no mirror")

mapn = {
    '1.1':'#','1.2':'#',
    '2.1':'.','2.2':'.'
}
assert detect_mirror(mapn,2,2) == 1
mapn = {
    '1.1':'#','1.2':'.',
    '2.1':'#','2.2':'.'
}
assert detect_mirror(mapn,2,2) == 100
mapn = {
    '1.1':'.','1.2':'.','1.3':'.',
    '2.1':'.','2.2':'#','2.3':'#',
    '3.1':'.','3.2':'.','3.3':'.'
}
assert detect_mirror(mapn,3,3) == 2
    
    
def day13(data):
    data.append("")
    obj = {}
    i = 0
    max_j = 0
    mirrors = 0
    textobj = ""
    for line in data:
        if line != "":
            textobj += "\n" + line
            i += 1
            max_j = len(line)
            for j,c in enumerate(line):
                obj[ij(i,j+1)] = c
        else:
            if len(obj) != 0:
                print(textobj)
                res = detect_mirror(obj, i, max_j)
                print("NEW DETECTION", res)
                mirrors += res
            i = 0
            obj = {}
            textobj = ""
    print(mirrors)
    return mirrors

assert day13(data_ex) == 405

start = time.time()
print("result", day13(data))
end = time.time()
print("Time : ", int(end - start), "s")



