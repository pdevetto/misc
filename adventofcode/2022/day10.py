import utils, sys, re
import functools
from itertools import product

def pf(k):
    [i,j] = k.split('.')
    return int(i), int(j)
def fp(i,j):
    return str(i) + '.' + str(j)

data_ex=[
    "noop",
    "addx 3",
    "addx -5"
]
data_ex2 = utils.readfile("data/d10_ex.txt")
data = utils.readfile("data/d10.txt")

def process_op(register, line):
    if line != "noop":
        command = line.split(" ")
        if command[0] == "addx":
            value = int(command[1])
            print("command=> ", line, value)
            yield register
            yield register + value
        else:
            print("ERROR", command)
            sys.exit(0)
    else:
        yield register
            

def d101(data):
    register = 1
    cycle = 0
    signal = 0
    steps = []
    for line in data:
        print(line)
        for reg in process_op(register, line):
            cycle += 1
            signal = cycle * register
            if cycle in [20, 60, 100, 140, 180, 220]:
                steps.append(signal)
            yield cycle, register
            print(cycle, register, signal)
            register = reg
            
            
        
def d102(data):
    crt = [""]
    line = 0
    for cycle, register in d101(data):
        if cycle%40 == 1:
            line += 1
            crt.append("")
        if cycle%40 in [ register, register+1, register+2 ]:
            crt[line] += "#"
        else:
            crt[line] += "."
    print("\n".join(crt))
    return crt

res = d102(data_ex2)
expected = [
"##..##..##..##..##..##..##..##..##..##..",
"###...###...###...###...###...###...###.",
"####....####....####....####....####....",
"#####.....#####.....#####.....#####.....",
"######......######......######......####",
"#######.......#######.......#######....."
]
print("-".join(expected))
print("-".join(res[1:7]))
#assert res[1:7] == expected
d102(data)

