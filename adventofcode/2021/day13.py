import utils, sys
data_exemple = ["6,10","0,14","9,10","0,3","10,4","4,11","6,0","6,12","4,1","0,13","10,12","3,4","3,0","8,4","1,10","2,14","8,10","9,0","","fold along y=7","fold along x=5"]
data_exo = utils.readfile("data/d13.txt")
#print(data_exemple)
#print(data_exo)

def pf(k):
    #print(k)
    [i,j] = k.split(',')
    return int(i), int(j)
def fp(i,j):
    return str(i) + ',' + str(j)

def process(data):
    coord = True
    maxi = 0
    maxj = 0
    coords = []
    for row in data:
        if len(row) == 0:
            coord = False
        elif coord:
            i,j = pf(row)
            if i > maxi:
                maxi = i
            if j > maxj:
                maxj = j
            coords.append(fp(i,j))
        else:
            print(coords)
            axis,value = row.split(" ")[2].split("=")
            print("fold ", axis, " - ", value)
            value = int(value)
            ncoords= coords.copy()
            for acoord in coords:
                x,y = pf(acoord)
                if axis == 'x' and x>value:
                    ncoords.remove(acoord)
                    nc = fp(value-(x-value),y)
                    ncoords.append(nc )
                if axis == 'y' and y>value:
                    ncoords.remove(acoord)
                    nc = fp(x,value-(y-value))
                    ncoords.append(nc )
            coords = list(set(ncoords))
            
    print(coords)
    print(len(coords))
    return coords
    
fcoord = process(data_exo)


print(fcoord)
maxx = 0 
maxy = 0
for coo in fcoord:
    x, y = pf(coo)
    #print(x, y)
    if maxx < x:
        maxx = x
    if maxy < y:
        maxy = y
print(maxx, maxy)

for j in range(0,6):
    stra = ""
    for i in range(0,39):
        if fp(i,j) in fcoord:
            stra += "#"
        else :
            stra += " "
    print(stra)
        
    