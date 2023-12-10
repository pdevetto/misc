import sys, re, time, numpy, collections, numpy

def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_ex= [
    ".....",
    ".S-7.",
    ".|.|.",
    ".L-J.",
    "....."
]
data_ex_2= [
    "..F7.",
    ".FJ|.",
    "SJ.L7",
    "|F--J",
    "LJ..."
]
data = readfile("data/d_2023_10.txt")


def ij2k(i=None,j=None,a=None):
    if a:
        i,j=a
    return str(i)+'.'+str(j)
assert ij2k(1,2) == '1.2'
assert ij2k(a=(1,2)) == '1.2'


def k2ij(k):
    return tuple(map(int,k.split('.')))
assert k2ij('1.2') == (1,2)

transfo = {
    '|':['-1.0',  '1.0'],
    '-':[ '0.-1', '0.1'],
    'L':['-1.0',  '0.1'],
    'J':['-1.0',  '0.-1'],
    '7':[ '0.-1', '1.0'],
    'F':[ '1.0',  '0.1'],
    'S':[ '1.0',  '0.1', '-1.0',  '0.-1'],
}


def add_tuple(a,b):
    return (a[0]+b[0],a[1]+b[1])
assert add_tuple((0,1),(2,3)) == (2,4)


def find_next_move(current, pipe, prev=None):
    #ij2k(a=k2ij(current) + k2ij(transfo))
    nexts = [ij2k(a=add_tuple(k2ij(current),k2ij(transfo))) for transfo in transfo[pipe]]
    if prev:
        return [next_e for next_e in nexts if next_e != prev]
    else:
        return nexts
assert find_next_move('4.6', 'J', '4.5') == ['3.6']

def map_parse(data):
    map_pipe = {}
    initial = 0
    for i,line in enumerate(data):
        for j,c in enumerate(line):
            if c != '.':
                map_pipe[ij2k(i,j)] = c
            if c == 'S':
                initial = ij2k(i,j)
    
    return initial, map_pipe

def day10(initial, map_pipe):
    previous = initial
    current = [pos for pos in find_next_move(initial,'S') if pos in map_pipe.keys()][0]
    map_loop = {initial:'S'}
    count = 1
    while count<100000:
        map_loop[current] = map_pipe[current]
        
        next_move = find_next_move(current,map_pipe[current],previous)[0]
        count += 1
        
        if next_move == initial:
            print(f"complete loop in {count}")
            return count/2, map_loop
        previous = current
        current = next_move
        
    raise Exception("Loop detected")    

initial, map_pipe = map_parse(data_ex)
assert day10(initial, map_pipe)[0] == 4
initial, map_pipe = map_parse(data_ex_2)
assert day10(initial, map_pipe)[0] == 8

start = time.time()
initial, map_pipe = map_parse(data)
print("result", day10(initial, map_pipe)[0])
end = time.time()
print("Time : ", int(end - start), "s")


data_ex_b_1 = [
    "...........",
    ".S-------7.",
    ".|F-----7|.",
    ".||.....||.",
    ".||.....||.",
    ".|L-7.F-J|.",
    ".|..|.|..|.",
    ".L--J.L--J.",
    "..........."
]
data_ex_b_2 = [
    ".F----7F7F7F7F-7....",
    ".|F--7||||||||FJ....",
    ".||.FJ||||||||L7....",
    "FJL7L7LJLJ||LJ.L-7..",
    "L--J.L7...LJS7F-7L7.",
    "....F-J..F7FJ|L7L7L7",
    "....L7.F7||L7|.L7L7|",
    ".....|FJLJ|FJ|F7|.LJ",
    "....FJL-7.||.||||...",
    "....L---J.LJ.LJLJ..."
]

def day10_b(data, s_pipe):
    initial, map_pipe = map_parse(data)    
    length,map_loop = day10(initial, map_pipe)
    
    print(length, map_loop)
    counter = 0
    for i,line in enumerate(data):
        print("*" * 10, "New line")
        inside = False
        loop = ""
        direction = ""
        for j,c in enumerate(line):
            print(c)
            if ij2k(i,j) in map_loop.keys():
                if c == 'S':
                    c = s_pipe
                if c == '|':
                    inside = not inside
                    print(f"changed > {inside}")
                if c == 'F':
                    direction = 'U'
                if c == 'L':
                    direction = 'D'
                if c == 'J' and direction == 'U':
                    inside = not inside
                if c == '7' and direction == 'D':
                    inside = not inside
                print(f"in the loop [{c}] {direction} - {inside}")
            else:
                if inside:
                    counter += 1            
                    print(f"Thing inside")
                
    print(f" counted {counter}")
    return counter
    
assert day10_b(data_ex_b_1, 'F') == 4
assert day10_b(data_ex_b_2, 'F') == 8
start = time.time()
print("result", day10_b(data, '7'))
end = time.time()
print("Time : ", int(end - start), "s")
