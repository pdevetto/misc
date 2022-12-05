import utils, sys, re
import functools

data_ex=[
    "    [D]    ",
    "[N] [C]    ",
    "[Z] [M] [P]",
    " 1   2   3 ",
    "",
    "move 1 from 2 to 1",
    "move 3 from 1 to 3",
    "move 2 from 2 to 1",
    "move 1 from 1 to 2",
]
data = utils.readfile("data/d5.txt")
print(data_ex)

a = [1,2,3,4]
b = a.pop(0)
c = a.pop(0)

print( a, " and ", b, " and ", c)
print([i for i in range(0, 4)])

def move_stack(stacks, n, source, dest):
    if not dest in stacks.keys():
        print("key not in")
        stacks[dest] = []
    #print("move ", n, " crates from stack ", source, " to stack ", dest)
    s_src = stacks[source]
    s_dest = stacks[dest]
    for i in range(0, n):
        crate = s_src.pop(0)
        s_dest = [crate] + s_dest
        #print(" --  \n", s_src, "\n", s_dest)
    stacks[source] = s_src
    stacks[dest] = s_dest
    return stacks

def move_stack_9001(stacks, n, source, dest):
    if not dest in stacks.keys():
        print("key not in")
        stacks[dest] = []
    #print("move ", n, " crates from stack ", source, " to stack ", dest)
    s_src = stacks[source]
    s_dest = stacks[dest]
    crate_list = s_src[0:n]
    new_src = s_src[n:]
    s_dest = crate_list + s_dest
    stacks[source] = new_src
    stacks[dest] = s_dest
    return stacks

assert move_stack({0:["A","B"], 1:["C", "D"]}, 1, 0, 1), {0:["B"], 1:["A", "C", "D"]}
assert move_stack({0:["A","B"], 1:["C", "D"]}, 2, 0, 1), {0:[], 1:["B", "A", "C", "D"]}
assert move_stack_9001({0:["A","B"], 1:["C", "D"]}, 1, 0, 1), {0:["B"], 1:["A", "C", "D"]}
assert move_stack_9001({0:["A","B"], 1:["C", "D"]}, 2, 0, 1), {0:[], 1:["A", "B", "C", "D"]}



def d051(data):
    stacks = {}
    fill_step = 0
    for line in data: 
        if len(line) == 0:
            print("end of fill")
            fill_step = 1
        if fill_step == 0:
            pattern = '.{3} ?'
            cut = re.findall(pattern, line)
            for i,block in enumerate(cut):
                #print(i,block)
                bloc = re.findall('\[([A-Z])\]', block)
                if len(bloc) != 0:
                    stacks = dict_append(stacks, i+1, bloc[0])
            print(stacks)
        else:
            pattern = 'move ([0-9]*) from ([0-9]*) to ([0-9]*)'
            cut = re.findall(pattern, line)
            if len(cut) != 0:
                (n, source, dest) = cut[0]
                stacks = move_stack_9001(stacks, int(n), int(source), int(dest))
                #print(stacks)
            
    word = ""
    for i in range(0, len(stacks)):
        word += stacks[i+1][0]
    print(word)

d051(data_ex)
d051(data)


