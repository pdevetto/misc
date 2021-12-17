# -*- coding: utf-8 -*-

from utils import *

def process_v1(commands):
    x, z, a = 0, 0, 0
    for command in commands:
        verb, value = command.split(" ")
        if verb == "forward":
            x += int(value)
        if verb == "up":
            z -= int(value)
        if verb == "down":
            z += int(value)
        print(command, ",", x, ",", z, ",", a)
    return x,z

r = process_v1(["forward 5","down 5","forward 8","up 3","down 8","forward 2"])
print(r)

a = file_input("/home/pierre/organisation/misc/advent21/data/d02.txt")
#process(a)

def process_v2(commands):
    x, z, a = 0, 0, 0
    for command in commands:
        verb, value = command.split(" ")
        if verb == "forward":
            x += int(value)
            z += a * int(value)
        if verb == "up":
            a -= int(value)
        if verb == "down":
            a += int(value)
        #print(command, ",", x, ",", z, ",", a)
    return x,z

r = process_v2(["forward 5","down 5","forward 8","up 3","down 8","forward 2"])
print(r)

a = file_input("/home/pierre/organisation/misc/advent21/data/d02.txt")
process_v2(a)