import utils, sys, re
import time, numpy, collections, itertools

data_ex = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
data = utils.readfile("data/d_2023_15.txt")[0]


def hash(word):
    hash = 0
    for character in word:
        hash = ((hash+ord(character)) * 17) % 256
    return hash

assert hash("HASH") == 52
def day15(data):
    sumhash = 0
    for word in data.split(","):
        wordhash = hash(word)
        print("word :", word, " = ", wordhash)
        sumhash += wordhash
    return sumhash

assert day15(data_ex) == 1320

start = time.time()
print("result", day15(data))
end = time.time()
print("Time : ", (end - start) * 1000, " ms")