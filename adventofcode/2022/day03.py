import json, re
from collections import Counter
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content
    
data_exemple = [
    "vJrwpWtwJgWrhcsFMMfFFhFp",
    "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
    "PmmdzqPrVvPwwTWBwg",
    "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
    "ttgJtRGJQctTZtZT",
    "CrZsJsPPZsGzwwsLwLmpwMDw"
]

def get_prio(lett):
    if lett == lett.lower():
        return ord(lett)-96
    else:
        return ord(lett)-38
    
assert(get_prio("a")== 1)
assert(get_prio("z")== 26)
assert(get_prio("A")== 27)
assert(get_prio("Z")== 52)

def d031( data):
    sump = 0
    for line in data:
        print(line)
        left = line[:len(line)//2]
        righ = line[len(line)//2:]
        print(set(left).intersection(set(righ)))
        inter = set(left).intersection(set(righ))
        for lett in inter:
            sump += get_prio(lett)
    print(sump)
        
#d031(data_exemple)
#d031(readfile("d03.txt"))

def d032( data):
    sump = 0
    groups = []
    for line in data:
        groups.append(line)
        if len(groups) == 3:
            int1 = set(groups[0]).intersection(set(groups[1]))
            int2 = int1.intersection(set(groups[2]))
            print(int2)
            for lett in int2:
                sump += get_prio(lett)
            groups = []
        
        
        
                        
    print(sump)
        
d032(data_exemple)
d032(readfile("d03.txt"))
