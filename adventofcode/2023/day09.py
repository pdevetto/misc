import sys, re, time, numpy, collections, numpy

def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_ex= [
"0 3 6 9 12 15",
"1 3 6 10 15 21",
"10 13 16 21 30 45"
]
data = readfile("data/d_2023_09.txt")

def day09(data):
    histories = 0
    previousies = 0
    for line in data:
        steps = []
        current = 0
        steps.append(list(map(int,line.split(" "))))
        all_zeroes = False
        
        while not all_zeroes:
            all_zeroes = True
            steps.append([])
            for i in range(0,len(steps[current]) -1):
                incr = steps[current][i+1] - steps[current][i]
                if incr != 0:
                    all_zeroes = False
                steps[current+1].append( incr )
            current += 1
        print(steps)
        for i in range(len(steps)-2, -1, -1):
            print("i", i)
            next_nb = steps[i][-1] + steps[i+1][-1]
            if i != 0:
                steps[i].append(next_nb)
            else:
                histories += next_nb
                print(f"history {next_nb}")
        for i in range(len(steps)-2, -1, -1):
            print("i", i)
            prev_nb = steps[i][0] - steps[i+1][0]
            if i != 0:
                steps[i] = [prev_nb] + steps[i]
            else:
                previousies += prev_nb
                print(f"previous {prev_nb}")
    print(histories, previousies)
    return (histories, previousies)
            
    

assert day09(data_ex) == (114, 2)
start = time.time()
print("result", day09(data))
end = time.time()
print("Time : ", int(end - start), "s")