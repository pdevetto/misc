import utils
data_exemple = [3,4,3,1,2]
data_exo = [x for x in map(lambda x: int(x), utils.readfile("data/d06.txt")[0].split(","))]
#print(data_exemple)
#print(data_exo)

def anotherday(lanternfishs):
    next_lfshs = []
    for lf in lanternfishs:
        if lf == 0:
            next_lfshs.append(6)
            next_lfshs.append(8)
        else:
            next_lfshs.append(lf-1)
    return next_lfshs

def life(lanternfishs, days):
    for i in range(1,days+1):
        lanternfishs = anotherday(lanternfishs)
        #print(i, ":", lanternfishs)
    print("final: ", len(lanternfishs))

#life(data_exemple, 256)
#life(data_exo, 80)

def anotherdayv2(lanternfishs):
    new_count_lfs = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
    for lf,coun in lanternfishs.items():
        if lf == 0:
            new_count_lfs[6]+=coun
            new_count_lfs[8]+=coun
        else:
            new_count_lfs[lf-1]+=coun
    return new_count_lfs
    
def lifev2(lanternfishs, days):
    count_lfs = {}
    for lf in lanternfishs:
        if not lf in count_lfs:
            count_lfs[lf]=0
        count_lfs[lf]+=1
    for i in range(1,days+1):
        count_lfs = anotherdayv2(count_lfs)
    print("final: ", count_lfs)
    print(sum(count_lfs.values()))

lifev2(data_exo, 256)