
import utils

data_exemple = ["0,9 -> 5,9",
"8,0 -> 0,8",
"9,4 -> 3,4",
"2,2 -> 2,1",
"7,0 -> 7,4",
"6,4 -> 2,0",
"0,9 -> 2,9",
"3,4 -> 1,4",
"0,0 -> 8,8",
"5,5 -> 8,2"]
data_exo = utils.readfile("data/d05.txt")

def drawmap(rules):
    dmap = {}
    for rule in rules:
        #print (rule)
        ruled = rule.split(" -> ")
        coord_a = ruled[0].split(",")
        coord_b = ruled[1].split(",")
        mini = min(int(coord_a[0]), int(coord_b[0]))
        maxi = max(int(coord_a[0]), int(coord_b[0]))
        minj = min(int(coord_a[1]), int(coord_b[1]))
        maxj = max(int(coord_a[1]), int(coord_b[1]))
        #print( mini, maxi, minj, maxj  )
        if not (mini != maxi and minj != maxj):
            for i in range(mini, maxi+1):
                for j in range(minj, maxj+1):
                    coo = str(i)+"."+str(j)
                    #print("coo" + coo)
                    if not coo in dmap:
                        dmap[coo] = 0
                    dmap[coo] += 1 
        if maxi-mini == maxj-minj:
            #print("rule : ", rule)
            a0 = int(coord_a[0])
            b0 = int(coord_b[0])
            step0 = 1 if b0>=a0 else -1
            a1 = int(coord_a[1])
            b1 = int(coord_b[1])
            step1 = 1 if b1>=a1 else -1
            #print("step1",step1)
            for i in range(a0, b0+step0, step0):
                counter = a1 + abs(i-a0)*step1
                #print("a1", a1, " i", i, " a0", a0, " counter", counter)
                coo = str(i)+"."+str(counter)
                #print("coo" + coo)
                if not coo in dmap:
                    dmap[coo] = 0
                dmap[coo] += 1 

        
    return dmap

themap = drawmap(data_exo)
#print(themap)
ones = [x for x in filter(lambda x: int(x)>=1, themap.values())]
print("ones")
print(len(ones))
twos = [x for x in filter(lambda x: int(x)>=2, themap.values())]
print("twos")
print(len(twos))
    