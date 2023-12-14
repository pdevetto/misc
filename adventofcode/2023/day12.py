import sys, re, time, numpy, collections, numpy

def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

data_ex= [
    "???.### 1,1,3",
    ".??..??...?##. 1,1,3",
    "?#?#?#?#?#?#?#? 1,3,1,6",
    "????.#...#... 4,1,1",
    "????.######..#####. 1,6,5",
    "?###???????? 3,2,1"
]
data = readfile("data/d_2023_12.txt")

def fit_line(row, groups):
    arrangs = [ '.', '#' ] if row[0] == '?' else [row[0]]
    min_char = sum(groups)+len(groups)-1
    len_row = len(row)
    for i,c in enumerate(row[1:]):
        last = i == len(row)-2
        #print(arrangs)
        #print(f"{last} CHAR {c} for {groups} -- {row}")
        next_arrangs = (list(map(lambda n: n+c, arrangs))
            if c != '?'
            else list(map(lambda n: n+".", arrangs)) + list(map(lambda n: n+"#", arrangs)))
        #print(next_arrangs)
        arrangs = []
        for arrg in next_arrangs:
            words_len = list(map(len, list(re.findall('(\#+)(?=[^#]|$)', arrg))))
            #print(f"   WORDS in {arrg} => {words_len}")
            restant_a_placer = (min_char - (sum(words_len)+len(words_len)))
            place_restante = len_row - len(arrg)
            too_late = place_restante < restant_a_placer
            if too_late: 
                #print(f"        toolate : reste {restant_a_placer} place {place_restante}")
                pass
            compare_grp = groups[0:len(words_len)]
            if arrg[-1] == '.':
                if words_len == compare_grp and not too_late:
                    arrangs.append(arrg)
            else:
                if words_len[:-1] == compare_grp[:-1] and words_len[-1] <= compare_grp[-1] and not too_late:
                    arrangs.append(arrg)
            
    return len(arrangs)
            
#assert fit_line("???.###", [1,1,3]) == 1
#assert fit_line(".??..??...?##.", [1,1,3]) == 4
#assert fit_line("?###????????", [3,2,1]) == 10

def day12(data):
    n = 0
    for line in data:
        row,groups = line.split(" ")
        groups = list(map(int,groups.split(',')))
        print("-"* 10, "\n", row, groups)
        n += fit_line(row, groups)
    return n

#assert day12(data_ex) == 21

start = time.time()
#print("result", day12(data))
end = time.time()
print("Time : ", int(end - start), "s")



def fit_line_v2(row, groups):
    arrangs = [ ('.',1), ('#',1) ] if row[0] == '?' else [(row[0], 1)]
    min_char = sum(groups)+len(groups)-1
    len_row = len(row)
    for i,c in enumerate(row[1:]):
        last = i == len(row)-2
        next_arrangs = (list(map(lambda n: (n[0]+c, n[1]), arrangs))
            if c != '?'
            else list(map(lambda n: (n[0]+'.', n[1]), arrangs))
                        + list(map(lambda n: (n[0]+'#', n[1]), arrangs)))
        arrangs = {}
        for j,arrg in enumerate(next_arrangs):
            words_len = list(map(len, list(re.findall('(\#+)(?=[^#]|$)', arrg[0]))))
            restant_a_placer = (min_char - (sum(words_len)+len(words_len)))
            place_restante = len_row - len(arrg[0])
            too_late = place_restante < restant_a_placer
            if too_late: 
                #print(f"        toolate : reste {restant_a_placer} place {place_restante}")
                pass
            compare_grp = groups[0:len(words_len)]
            if arrg[0][-1] == '.':
                if words_len == compare_grp and not too_late:
                    key = '_'.join(map(str,words_len))
                    if not key in arrangs:
                        arrangs[key] = arrg
                    else:
                        arrangs[key] = (arrangs[key][0], arrangs[key][1] + arrg[1])
            else:
                if words_len[:-1] == compare_grp[:-1] and words_len[-1] <= compare_grp[-1] and not too_late:
                    arrangs["full"+str(j)] = arrg
        arrangs = arrangs.values()
    return sum( map(lambda arrg: arrg[1], arrangs) )
            
#assert fit_line_v2("???.###????.###????.###????.###????.###", [1,1,3,1,1,3,1,1,3,1,1,3,1,1,3]) == 1
assert fit_line_v2(".??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.",
                   [1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3]) == 16384

def day12_b(data):
    n = 0
    line_count = 0
    for line in data:
        line_count += 1
        row,groups = line.split(" ")
        groups = list(map(int,groups.split(',')))
        
        row5 = '?'.join([ row ] * 5)
        gp5 = groups + groups +  groups + groups + groups
        
        print("LINE ", line_count, row5, gp5)
        result = fit_line_v2(row5, gp5)
        n+= result
        print(" > ", result)
        
        
    return n

assert day12_b(data_ex) == 525152

start = time.time()
print("result", day12_b(data))
end = time.time()
print("Time : ", int(end - start), "s")



