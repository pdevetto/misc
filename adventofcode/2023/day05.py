import utils, sys, re, functools
import time

data_ex= [
    "seeds: 79 14 55 13",
    "",
    "seed-to-soil map:",
    "50 98 2",
    "52 50 48",
    "",
    "soil-to-fertilizer map:",
    "0 15 37",
    "37 52 2",
    "39 0 15",
    "",
    "fertilizer-to-water map:",
    "49 53 8",
    "0 11 42",
    "42 0 7",
    "57 7 4",
    "",
    "water-to-light map:",
    "88 18 7",
    "18 25 70",
    "",
    "light-to-temperature map:",
    "45 77 23",
    "81 45 19",
    "68 64 13",
    "",
    "temperature-to-humidity map:",
    "0 69 1",
    "1 0 69",
    "",
    "humidity-to-location map:",
    "60 56 37",
    "56 93 4"
]
data = utils.readfile("data/d_2023_05.txt")

step_path = {'seed':'soil', 'soil':'fertilizer', 'fertilizer':'water', 'water':'light', 
            'light':'temperature', 'temperature':'humidity', 'humidity':'location'}
def get_map(data):
    maps = {}
    step = ""
    for line in data:
        if step == "" and re.match('seeds:.*', line):
            maps["seed"] = [int(n) for n in re.findall('([0-9]+)', line)]
        else:
            is_next_step = re.findall('([a-z]*)-to-([a-z]*) map:', line)
            if is_next_step:
                #print(f"new step : {is_next_step}")
                if step_path[is_next_step[0][0]] == is_next_step[0][1]:
                    step = is_next_step[0][1]
            elif line != "":
                [dest, src_start, src_range] = line.split(" ")
                src_start = int(src_start)
                src_end = int(src_start)+int(src_range)-1
                #print(f"nbs : {dest} from {src_start} to {src_end}")
                if not step in maps:
                    maps[step] = []
                maps[step].append((src_start,src_end,int(dest)))
    return maps

def day05(maps):
    step = "seed"
    objects = maps["seed"]    
    while step in step_path.keys():
        dest_objects = []
        destination = step_path[step]
        #print("dest",destination, maps[destination])
        for obj in objects:
            #print("obj",obj)
            dests = [dest for dest in maps[destination] if obj >= dest[0] and obj <= dest[1]]
            #print(dests)
            if len(dests) == 1:            
                dests = dests[0]
                newobj = dests[2] + (obj - dests[0])
                dest_objects.append(newobj)
            else: 
                dest_objects.append(obj)
        print(dest_objects, "\n", "*" * 20)
        step = destination
        objects = dest_objects
            
    
    return min(dest_objects)    
    print(maps)

def cross_interval(i, j, revert=False):
    if i[0] <= j[0] <= j[1] <= i[1]:
        return (j[0],j[1])
    if i[0] <= j[0] and j[0] <= i[1]:
        return (j[0],i[1])
    if not revert:
        return cross_interval(j, i, True)
    return None

assert cross_interval((0,5),(2,3)) == (2,3)
assert cross_interval((2,3),(0,5)) == (2,3)
assert cross_interval((0,5),(3,7)) == (3,5)
assert cross_interval((3,7),(0,5)) == (3,5)
assert cross_interval((0,5),(10,15)) == None

def new_interval(intervals, i1, i2):
    if i1<i2:
        intervals.append((i1,i2))
    return intervals

def day05_b(maps, data):
    intervals = []
    step = "seed"
    whilecount = 0
    print(data[0])
    for couple in re.findall('([0-9]+ [0-9]+)', data[0]):
        a,b = tuple(map(int,couple.split(" ")))
        intervals.append((a,a+b-1))
    print(intervals)
    while step in step_path.keys():
        dest_intervals = []
        destination = step_path[step]
        print("dest",destination, maps[destination])
        for dest in maps[destination]:
            safe_intervals = []
            while len(intervals) != 0:
                whilecount += 1
                itrvl = intervals[0]
                intervals = intervals[1:]
                overrides = cross_interval(itrvl, (dest[0], dest[1]))
                if overrides:
                    keep = True
                    intervals = new_interval(intervals, itrvl[0], overrides[0]-1)
                    intervals = new_interval(intervals, itrvl[1], overrides[1]-1)
                    dest_intervals.append((
                        overrides[0],
                        overrides[1],
                        dest[2]-dest[0]
                    ))
                else: 
                    safe_intervals.append(itrvl)
            intervals = safe_intervals
        print("dest", dest_intervals)
        print("int", intervals)
        for dest_i in dest_intervals:
            intervals.append((dest_i[0]+dest_i[2], dest_i[1]+dest_i[2]))
        
        print("*" * 20)
        step = destination
    print(intervals)
    print(list(map(lambda d: d[0], intervals)))
    print("While loop count ", whilecount)
    return min(list(map(lambda d: d[0], intervals)))
    
maps = get_map(data_ex)
assert day05(maps) == 35
assert day05_b(maps, data_ex) == 46

maps = get_map(data)
#day05(maps)
start = time.time()
print("result", day05_b(maps, data))
end = time.time()
print("Time : ", (end - start)*1000, " ms")
