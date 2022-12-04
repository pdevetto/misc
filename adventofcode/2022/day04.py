import json, re
from collections import Counter
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content
    
data_exemple = [
    "2-4,6-8",
    "2-3,4-5",
    "5-7,7-9",
    "2-8,3-7",
    "6-6,4-6",
    "2-6,4-8"
]

def isin(a,b,x,y):
    return int(a) >= int(x) and int(b) <= int(y)

assert(isin(1,4,0,5))
assert(not isin(0,4,1,5))
assert(isin(0,4,0,5))
assert(not isin(1,2,3,4))
    
def d041( data):
    contained = 0
    for line in data:
        pattern = ',|-'
        a,b,x,y = re.split(pattern, line)
        if isin(a,b,x,y):
            contained += 1
        elif isin(x,y,a,b):
            contained += 1
    print(contained)
        
#d041(data_exemple)
#d041(readfile("day04.txt"))

def overlap(a,b,x,y):
    return (int(a) >= int(x) and int(a) <= int(y)) or (int(b) >= int(x) and int(b) <= int(y)) or isin(x,y,a,b)

def d042( data):
    overlapped = 0
    for line in data:
        pattern = ',|-'
        a,b,x,y = re.split(pattern, line)
        print(a,b,x,y)
        if overlap(a,b,x,y):
            overlapped += 1
            print("==> Overlap")
    print(overlapped)

d042(data_exemple)
d042(readfile("day04.txt"))
