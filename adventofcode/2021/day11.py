import utils, sys
data_exemple = ["11111",
"19991",
"19191",
"19991",
"11111"]
da2 = ["5483143223",
"2745854711",
"5264556173",
"6141336146",
"6357385478",
"4167524645",
"2176841721",
"6882881134",
"4846848554",
"5283751526"]
data_exo = utils.readfile("data/d11.txt")
#print(data_exemple)
#print(data_exo)


def pf(k):
    [i,j] = k.split('.')
    return int(i), int(j)
def fp(i,j):
    return str(i) + '.' + str(j)

def get8ps(octs):
    mapocto = {}
    for i,octoline in enumerate(octs):
        for j,octo in enumerate([x for x in octoline]):
            mapocto[fp(i,j)] = int(octo)
    return mapocto

def process(mapocto):
    #print(mapocto)
    flash = []
    newflash = []
    for coord,lightlvl in mapocto.items():
        mapocto[coord] += 1
    #print(mapocto)
    newflash = [coord for coord,value in mapocto.items() if value>9]
    #print(newflash)
    keeplight = True
    while(keeplight):
        keeplight = False
        for coord in newflash:
            newflash.remove(coord)
            i,j = pf(coord)
            if not coord in flash:
                flash.append(coord)
                for nkey in [fp(i-1,j-1),fp(i-1,j),fp(i-1,j+1),
                            fp(i,j-1),           fp(i,j+1),
                            fp(i+1,j-1),fp(i+1,j),fp(i+1,j+1)]:
                    if nkey in mapocto.keys():
                        mapocto[nkey] += 1
                        if mapocto[nkey]>9:
                            newflash.append(nkey)
        #print("#########")
        #print(flash)
        #print(newflash)
        keeplight = len(newflash) != 0
    for coo in flash:
        mapocto[coo] = 0
    return len(flash),mapocto

def printmap(mapocto):
    print('------------')
    oldj = 0
    ch = ""
    for coo,val in mapocto.items():
        i,j = pf(coo)
        #print(i,j)
        if(oldj != i):
            print(ch)
            ch = ""
            oldj=i
        ch += str(val) + "."
    print(ch)
    
def propro(data_ex):
    mapocto = get8ps(data_ex)
    nc = 0
    for i in range(0,1000):
        fcount, mapocto = process(mapocto)
        nc += fcount
        print(i, " * = ", nc, " --", fcount)
        #printmap(mapocto)
        if fcount == 100:
            sys.exit()
    
        
propro(data_exo)
