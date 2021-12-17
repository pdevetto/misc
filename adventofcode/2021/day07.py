import utils
data_exemple = [16,1,2,0,4,2,7,1,2,14]
data_exo = [x for x in map(lambda x: int(x), utils.readfile("data/d07.txt")[0].split(","))]
print(data_exemple)
#print(data_exo)

def aligncrab(crabs):
    posmax = max(crabs)
    minfuel = -1
    minpos = -1
    for i in range(0, posmax+1):
        fuelpos = fuelforposv2(crabs, i)
        if minfuel == -1 or fuelpos<minfuel:
            minpos = i
            minfuel = fuelpos
            #print("pos", minpos, "fuel", minfuel)
    print("FINAL : pos", minpos, "fuel", minfuel)
    
def fuelforpos(crabs,pos):
    fuel = 0
    for currpos in crabs:
        fuel += abs(currpos - pos)
    return fuel

def arithmetic(n):
    return n*(n+1)/2
    
assert sumnumber(2) == 3
assert sumnumber(4) == 10
assert sumnumber(9) == 45

def fuelforposv2(crabs,pos):
    fuel = 0
    for currpos in crabs:
        fuel += arithmetic(abs(currpos - pos))
    return fuel


aligncrab(data_exemple)
aligncrab(data_exo)
        
        
        