import utils, sys, re, numpy, json
import functools
from itertools import product

data_ex = [
    "[1,1,3,1,1]",
    "[1,1,5,1,1]",
    "",
    "[[1],[2,3,4]]",
    "[[1],4]",
    "",
    "[9]",
    "[[8,7,6]]",
    "",
    "[[4,4],4,4]",
    "[[4,4],4,4,4]",
    "",
    "[7,7,7,7]",
    "[7,7,7]",
    "",
    "[]",
    "[3]",
    "",
    "[[[]]]",
    "[[]]",
    "",
    "[1,[2,[3,[4,[5,6,7]]]],8,9]",
    "[1,[2,[3,[4,[5,6,0]]]],8,9]",
]
data = utils.readfile("data/d13.txt")

def cleanup(obj):
    new_obj = []
    for i in obj:
        if not isinstance(i, list):
            new_obj.append(i)
        else:
            new_list = cleanup(i)
            if new_list != []:
                new_obj.append(new_list)
    return new_obj

print(cleanup([1,2,[[[]]]]) )
assert cleanup([1,2,[[[]]]]) == [1,2]

def get_cpxidx(obj, idx):
    print ("GCX", obj, idx)
    cur_obj = obj
    for i in idx:
        if not isinstance(cur_obj, list):
            if i == 0:
                return cur_obj
            return None
        elif cur_obj == []:
            return None
        ##cur_obj = cleanup(cur_obj)
        if i < len(cur_obj):
            cur_obj = cur_obj[i]
        else:
            return None
    return cur_obj

assert get_cpxidx([0,1,2], [1]) == 1
assert get_cpxidx([0,[],1,2], [1]) == []
assert get_cpxidx([0,[[[]]],1,2], [2]) == 1
assert get_cpxidx([0,[[[[[6]]]]],1,2], [1]) == [[[[[6]]]]]
assert get_cpxidx([0,[1,2]], [1,1]) == 2
assert get_cpxidx([0,[1,[2,3]]], [1,1,1]) == 3
assert get_cpxidx([0,[1,[2,3]]], [1,1]) == [2,3]


def comparepare(p_left, p_right):
    cpxidx = [-1]
    status = True
    while status:
        if cpxidx == []:
            return 0
        cpxidx[-1]=cpxidx[-1]+1
        e_left = get_cpxidx(p_left,cpxidx)
        e_right = get_cpxidx(p_right,cpxidx)
        if e_left == None and e_right == None:
            cpxidx=cpxidx[:-1]
        elif e_left == None:
            return -1
        elif e_right == None:
            return 1
        else:
            if isinstance(e_left, list) and not isinstance(e_right, list):
                e_right = [e_right]
            if isinstance(e_right, list) and not isinstance(e_left, list):
                e_left = [e_left]
            # compare
            print("E : ", e_left, e_right)
            if isinstance(e_left, list) and isinstance(e_right, list):
                cpxidx.append(-1)
            else:
                if int(e_left) < int(e_right):
                    return -1
                elif int(e_left) > int(e_right):
                    return 1

assert comparepare([0,2,2], [0,1,2]) == 1
assert comparepare([0,1,2], [0,2,2]) == -1
assert comparepare([0,1,2], [0,1,2]) == 0
assert comparepare([0,1], [0,1,2]) == -1
assert comparepare([0,1,2], [0,1]) == 1
assert comparepare([0,1,2], [0,1,[]]) == 1

assert comparepare([0,1,2], [0,1,[]]) == 1

assert comparepare([6,7],
                   [6,0]) == 1
assert comparepare([6], [6,0]) == -1
assert comparepare([6,[]], [6,0]) == -1
assert comparepare([[6], [], [7]],
                   [[6, 0]]) == -1
assert comparepare([[0]],
                   [[0], [[]]]) == -1


def d131(data):
    p1 = None
    p2 = None
    right_ordrered =  []
    indice = 0
    print("\n\n P", indice+1)
    for line in data:
        if line == "":
            print("\n\n P", indice+1)
            p1 = None
            p2 = None
        elif p1 == None:
            print(line)
            p1 = json.loads(line)
        else:
            print(line)
            p2 = json.loads(line)
            indice += 1
            order = comparepare(p1, p2)
            if order == -1:
                print("ORDERED ", indice)
                right_ordrered.append(indice)

    return right_ordrered

#pairs = d131(data_ex)
#print(pairs, " = ", sum(pairs))

#pairs = d131(data)
#print(pairs, " = ", sum(pairs))

def d132(data):
    pairs = []
    for line in data:
        if line.strip() != "":
            pairs.append(json.loads(line))
    pairs.append([[2]])
    pairs.append([[6]])
    print(pairs)
    print ("---")
    pairs.sort(key=functools.cmp_to_key(comparepare))
    print ("---")
    d1 = 0
    d2 = 0

    for i,pair in enumerate(pairs):
        if pair == [[2]]:
            d1 = i+1
        if pair == [[6]]:
            d2 = i+1
        print(pair)
    print ("---", d1, d2, d1*d2)
    return d1,d2


assert d132(data_ex) == (10,14)
d132(data)
