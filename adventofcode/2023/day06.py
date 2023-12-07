import utils, sys, re, functools
import time, numpy

data_ex= ["Time:      7  15   30",
        "Distance:  9  40  200"]
data = ["Time:        58     81     96     76",
        "Distance:   434   1041   2219   1218"]

def day06(data):
    data_time = re.findall("([0-9]+)", data[0])
    data_distance = re.findall("([0-9]+)", data[1])
    return numpy.prod([
        len([i 
            for i in range(1, int(a_time)+1) 
             if i*(int(a_time)-i) > int(data_distance[race])])
        for race,a_time in enumerate(data_time)
    ])
    
data_ex2= ["Time:      71530",
        "Distance:  940200"]
data2 = ["Time:        58819676",
        "Distance:   434104122191218"]

def day06_b(data):
    data_time = int(re.findall("([0-9]+)", data[0])[0])
    data_distance = int(re.findall("([0-9]+)", data[1])[0])
    return len([i for i in range(1, data_time+1) if i*(data_time-i) > data_distance])


assert day06(data_ex) == 288
print("results", day06(data))

assert day06_b(data_ex2) == 71503
start = time.time()
print("result", day06_b(data2))
end = time.time()
print("Time : ", (end - start)*1000, " ms")
