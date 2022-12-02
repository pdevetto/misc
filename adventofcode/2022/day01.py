import utils

data_exemple = ["1000","2000","3000","","4000","","5000","6000","","7000","8000","9000","","10000"]
data = utils.readfile("data/d1.txt")

#print(data_exemple)
#print(data)

def dict_plusplus(data, i, val):
    if not i in data.keys():
        data[i] = 0
    data[i]+= val
    return data

def d010(data):
    print(data)
    elves = {}
    start = 0
    for line in data:
        if len(line) == 0 or int(line) == 0:
            start += 1
        else :
            elves = dict_plusplus(elves, start, int(line))
    #print(elves)
    return elves

res = d010(data_exemple)
print(max(res.values()))

res2 = d010(data)
print(max(res2.values()))

calories = list(res2.values())
calories.sort()
print(calories[-3:])
print(sum(calories[-3:]))
