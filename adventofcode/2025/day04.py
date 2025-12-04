import utils
import re 

data_ex = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]
data = utils.readfile("data/d04.txt")

sides = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

def day04(data):
    spots = {}
    access = 0
    for i,line in enumerate(data):
        for j,spot in enumerate(line):
            if spot == '@':
                utils.dict_append(spots, utils.xy2k(i,j), spot)
    for k, spot in spots.items():
        x,y = utils.k2xy(k)
        has_side = sum(list(map(lambda delta: utils.xy2k(x+delta[0], y+delta[1]) in spots, sides)))
        access += 1 if has_side<4 else 0
    return access

assert day04(data_ex) == 13
print(day04(data))

def day04b(data):
    spots = {}
    removed = 0
    for i,line in enumerate(data):
        for j,spot in enumerate(line):
            if spot == '@':
                utils.dict_append(spots, utils.xy2k(i,j), spot)
    old_rolls = len(spots) + 1
    while len(spots) < old_rolls:
        old_rolls = len(spots)
        spot_items = spots.copy().items()
        for k, spot in spot_items:
            x,y = utils.k2xy(k)
            has_side = sum(list(map(lambda delta: utils.xy2k(x+delta[0], y+delta[1]) in spots, sides)))
            if has_side<4:
                del spots[k]
                removed += 1
    print( removed , " rolls removed")
    return removed

assert day04b(data_ex) == 43
print(day04b(data))