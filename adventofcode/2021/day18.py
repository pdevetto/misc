import json, re
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_exemple = [
"[1,2]"
"[[1,2],3]"
"[9,[8,7]]"
"[[1,9],[8,5]]"
"[[[[1,2],[3,4]],[[5,6],[7,8]]],9]",
"[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]",
"[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"]

data_exo = readfile("data/d18.txt")
print(data_exemple)
#print(data_exo)

def sn_split(number):
    petitmilieu = int(number/2)
    return [ petitmilieu, number - petitmilieu ]

assert sn_split(10) == [5,5]
assert sn_split(11) == [5,6]

def look_split(number):
    nbstr = json.dumps(number)
    listnbs = [x for x in filter(lambda x: x!='', re.split(r'[^0-9]+', nbstr))]
    for nb in listnbs:        
        if int(nb) >= 10:
            newnb_str = json.dumps(sn_split( int(nb) ))
            return json.loads( nbstr.replace(str(nb), newnb_str, 1) )
    return False
    
assert look_split([10,8]) == [[5,5],8]
assert look_split([2,8]) == False
assert look_split([[10,8],10]) == [[[5,5],8],10]
                              
def get_start(nb,i):
    if nb >= 100:
        return i-2
    if nb >= 10:
        return i-1
    return i

def look_explode(number):
    nbstr = json.dumps(number)
    newchain = []
    count = 0
    lastn_index = {
        0: [-1,-1,-1],
        1: [-1,-1,-1],
        2: [-1,-1,-1]
    }
    cn = 0
    ispair = False
    isnumber = False
    pair = []
    
    for i,cha in enumerate([x for x in nbstr]):
        if cha=='[':
            count += 1
            pair = []
            ispair = True
        if cha == ',':
            if ispair:
                pair.append(cn)
            
        if cha in [',',']'] and isnumber:
            lastn_index[2] = lastn_index[1]
            lastn_index[1] = lastn_index[0]
            lastn_index[0] = [cn, get_start(cn, i-1), i-1]
            cn = 0
        if cha in ['0','1','2','3','4','5','6','7','8','9']:
            cn = (cn*10 + int(cha))
            isnumber = True
        else:
            isnumber = False
        if cha == ']':
            if ispair:
                if count > 4:
                    #print(f"explode {lastn_index}")
                    lastn,last_a,last_z = lastn_index[2]
                    left,left_a,left_z = lastn_index[1]
                    right,right_a,right_z = lastn_index[0]
                    if lastn != -1:
                        newchain = nbstr[0:last_a] + str(lastn+left) + nbstr[last_z+1:left_a-1]
                    else:
                        newchain = nbstr[0:left_a-1]
                    newchain += "0"
                    reste = nbstr[right_z+2:]
                    remainnumbs = [x for x in filter(lambda x: x!='', re.split(r'[^0-9]+', json.dumps(reste)))]
                    if len(remainnumbs)>=1:
                        newchain += reste.replace(str(remainnumbs[0]), str(int(remainnumbs[0])+right), 1)
                    else: 
                        newchain += reste
                    #print('newchaine', newchain)
                    return json.loads(newchain)
            count-=1
            ispair=False
        
    return False

assert look_explode([1,2]) == False
assert look_explode([[[[[1,2]]]]]) == [[[[0]]]]
assert look_explode([[4,[[[[1,2]]]]],6]) == [[5,[[[0]]]],8]
assert look_explode([[[[[9,8],1],2],3],4]) == [[[[0,9],2],3],4]
assert look_explode([7,[6,[5,[4,[3,2]]]]]) == [7,[6,[5,[7,0]]]]
assert look_explode([[6,[5,[4,[3,2]]]],1]) == [[6,[5,[7,0]]],3]
assert look_explode([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
assert look_explode([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]) == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

def sn_reduce(number):
    keep = True
    while keep:
        newnumb = look_explode(number)
        if newnumb != False:
            number = newnumb
            keep = True
        else:
            newnumb = look_split(number)
            if newnumb != False:
                number = newnumb
                keep = True
            else:
                return number

assert sn_reduce([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]) == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]

def process(numbers):
    mynumber = numbers[0]
    for number in numbers[1:]:
        mynumber = sn_reduce([mynumber, number])
        print("#### ")
        print(number)
        print(mynumber)
    return mynumber
        

assert process([
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
    [7,[5,[[3,8],[1,4]]]],
    [[2,[2,2]],[8,[8,1]]],
    [2,9],
    [1,[[[9,3],9],[[9,0],[0,7]]]],
    [[[5,[7,4]],7],1],
    [[[[4,2],2],6],[8,7]]
]) ==  [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]

def magnitude(nb):
    if isinstance(nb, int):
        return nb
    else: 
        return 3*magnitude(nb[0]) + 2*magnitude(nb[1])


assert magnitude([[1,2],[[3,4],5]] ) ==  143.
assert magnitude([[[[0,7],4],[[7,8],[6,0]]],[8,1]] ) ==  1384.
assert magnitude([[[[1,1],[2,2]],[3,3]],[4,4]] ) ==  445.
assert magnitude([[[[3,0],[5,3]],[4,4]],[5,5]] ) ==  791.
assert magnitude([[[[5,0],[7,4]],[5,5]],[6,6]] ) ==  1137.
assert magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]] ) ==  3488.


assert( magnitude( [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]] )) == 4140

print("END")

#print(magnitude( process ([ json.loads(x) for x in data_exo ]) ))

datas = [ json.loads(x) for x in data_exo ]

maxmagn = 0
for i,x in enumerate(datas):
    for j,y in enumerate(datas):
        print(i,j)
        if i != j:
            magn = magnitude( sn_reduce( [x, y] ) )
            if magn > maxmagn:
                maxmagn = magn

print("maxmagn", maxmagn)
