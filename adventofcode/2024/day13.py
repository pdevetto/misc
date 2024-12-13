import utils, re
import itertools
from dataclasses import dataclass
import numpy as np

data_ex = [
    "Button A: X+94, Y+34",
    "Button B: X+22, Y+67",
    "Prize: X=8400, Y=5400",
    "",
    "Button A: X+26, Y+66",
    "Button B: X+67, Y+21",
    "Prize: X=12748, Y=12176",
    "",
    "Button A: X+17, Y+86",
    "Button B: X+84, Y+37",
    "Prize: X=7870, Y=6450",
    "",
    "Button A: X+69, Y+23",
    "Button B: X+27, Y+71",
    "Prize: X=18641, Y=10279",
]

data = utils.readfile("data/day13.txt")

@dataclass()
class Machine:
    A_x: int
    A_y: int
    B_x: int
    B_y: int
    P_x: int
    P_y: int


def parse_data13(data)->list[Machine]:
    machines = []
    data = "\n".join(data)
    machine_re = re.compile(r"Button A: X\+([0-9]*), Y\+([0-9]*)\nButton B: X\+([0-9]*), Y\+([0-9]*)\nPrize: X=([0-9]*), Y=([0-9]*)", re.MULTILINE)
    parsed_machines = machine_re.findall(data)
    for mac in parsed_machines:
        machines.append(Machine( *tuple(map(int,mac)) ))

    print(machines)
    return machines

assert parse_data13(["Button A: X+94, Y+34","Button B: X+22, Y+67","Prize: X=8400, Y=5400"]) == [Machine(A_x=94, A_y=34, B_x=22, B_y=67, P_x=8400, P_y=5400)]

def valid(machine, a, b):
    return (
        int(a) * machine.A_x + int(b) * machine.B_x == machine.P_x
    )
    

def day13(data, part2= False):
    tokens = 0
    tokens_2 = 0
    for machine in parse_data13(data):
        a= np.array([[machine.A_x, machine.B_x], [machine.A_y, machine.B_y]])
        b= np.array([machine.P_x, machine.P_y])
        
        x = np.linalg.solve(a, b)
        if ( 0 <= int(x[0]) <= 100 and 0 <= int(x[1]) <= 100 ):
            ia = int(x[0])
            ib = int(x[1])
            if valid( machine, x[0], x[1]):
                tokens += ia * 3 + ib
            elif valid( machine, ia+1, ib):
                tokens += (ia+1)*3 + ib
            elif valid( machine, ia, ib+1):
                tokens += ia*3 + (ib+1)
            #print( " XX ", x, " = ", int(x[0])*3 + int(x[1]))
            else: 
                print( machine )
                print(" YY no iteger sol ", x, "  / ", 
                    int(x[0]) * machine.A_x + int(x[1]) * machine.B_x, " == ", machine.P_x, " / ", 
                    int(x[0]) * machine.A_y + int(x[1]) * machine.B_y, " == ", machine.P_y )
        if part2:
            P_x = machine.P_x + 10000000000000
            P_y = machine.P_y + 10000000000000
            sola = machine.B_y * P_x - machine.B_x * P_y
            solb = -machine.A_y * P_x + machine.A_x * P_y
            deter = machine.A_x * machine.B_y - machine.A_y * machine.B_x

            if sola % deter == 0 and solb % deter == 0:
                tokens_2 += int(sola/deter)*3 + int(solb/deter)
    return tokens, tokens_2
       
assert (day13(data_ex))[0] == 480
print(day13(data)[0])
# 28597 too low 

print("PART 2 ", "+"*100)
assert (day13(data_ex, True))
print(day13(data, True)[1])