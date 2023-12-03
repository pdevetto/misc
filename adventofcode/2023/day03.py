import json, re, time
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_ex = [ "467..114..",
            "...*......",
            "..35..633.",
            "......#...",
            "617*......",
            ".....+.58.",
            "..592.....",
            "......755.",
            "...$.*....",
            ".664.598.."]
data = readfile("data/d_2023_03.txt")

def pf(k):
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)

def day03(data):
    numbers = []
    for y,line in enumerate(data):
        for numb in re.finditer("([0-9]+)", line):
            borne_a = max(numb.start()-1, 0)
            borne_z = min(numb.end(), len(line)-1)
            size = len(numb.group())
            number = int(numb.group())
            #print(f"{y} + {number} + {borne_a} / {borne_z}")            
            coords = []
            if y>0:
                coords += [fp(x,y-1) for x in range(borne_a, borne_z+1)]
            if numb.start() > 0:
                coords += [fp(borne_a,y)]
            if numb.end() < len(line):
                coords += [fp(borne_z,y)]
            if y<len(data)-1:
                coords += [fp(x,y+1) for x in range(borne_a, borne_z+1)]        
            if set([data[pf(k)[1]][pf(k)[0]] for k in coords]) != {'.'}:
                numbers.append(number)
    return numbers 

nbs = day03(data_ex)
print(nbs)
assert sum(nbs) == 4361

print(sum(day03(data)))

def dict_append(data, i, val):
    if not i in data.keys():
        data[i] = []
    data[i].append(val)
    return data

def day03_b(data):
    gears = {}
    for y,line in enumerate(data):
        for numb in re.finditer("([0-9]+)", line):
            borne_a = max(numb.start()-1, 0)
            borne_z = min(numb.end(), len(line)-1)
            size = len(numb.group())
            number = int(numb.group())
            #print(f"{y} + {number} + {borne_a} / {borne_z}")            
            coords = []
            if y>0:
                coords += [fp(x,y-1) for x in range(borne_a, borne_z+1)]
            if numb.start() > 0:
                coords += [fp(borne_a,y)]
            if numb.end() < len(line):
                coords += [fp(borne_z,y)]
            if y<len(data)-1:
                coords += [fp(x,y+1) for x in range(borne_a, borne_z+1)]        
            for k in coords:
                if data[pf(k)[1]][pf(k)[0]] == '*':
                    gears = dict_append(gears, k, number)
    print(gears)
    ratios = 0
    for gear_nbs in gears.values():
        if len(gear_nbs) == 2:
            ratios += int(gear_nbs[0]) * int(gear_nbs[1])
            
    return ratios

nbs = day03_b(data_ex)
assert nbs == 467835

print(day03_b(data))
