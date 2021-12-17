import utils, sys
data_exemple = [
"be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
"edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
"fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
"fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
"aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
"fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
"dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
"bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
"egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
"gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"]
data_exo = utils.readfile("data/d08.txt")
print(data_exemple)
#print(data_exo)
        
def process(notes):
    uniqdig = 0
    for note in notes:
        inputs = note.split('|')
        digits = inputs[1].strip().split(" ")
        for digit in digits:
            if len(digit.strip()) in [2,3,4,7]:
                uniqdig += 1
    print(uniqdig)

process(data_exemple)
process(data_exo)

def computedigi(digit, mapl):
    if len(digit) == 2:
        return 1
    if len(digit) == 3:
        return 7
    if len(digit) == 4:
        return 4
    if len(digit) == 7:
        return 8
    if len(digit) == 6:
        if not mapl['d'] in digit:
            return 0
        if mapl['c'] in digit:
            return 9
        return 6
    if mapl['b'] in digit:
        return 5
    if mapl['e'] in digit:
        return 2
    return 3

#  a
# b c
#  d 
# e f 
#  g 

def onelineofnote(note):
    mapl = {'a':'','b':'','c':'','d':'','e':'','f':'','g':''}
    inputs = note.split('|')
    first = inputs[0].strip().split(" ")
    digits = inputs[1].strip().split(" ")
    
    dgt={}
    for digit in first:
        dlen = len(digit.strip())
        if not dlen in dgt:
            dgt[dlen] = []
        dgt[dlen].append(digit)
    #print( dgt)
    # 1 
    mapl['c']= list(dgt[2][0])
    mapl['f']= list(dgt[2][0])
    # 7
    mapl['a']= list(set(dgt[3][0]) - set(mapl['f']))[0]
    # 4
    mapl['b']= list(set(dgt[4][0]) - set(mapl['f']))
    mapl['d']= list(set(dgt[4][0]) - set(mapl['f']))
    # 2 3 5
    fiveclean = [x for x in map(lambda dg:list(set(dg) - set(mapl['a']) - set(mapl['f'])),dgt[5])]
    thethree = [x for x in filter(lambda dg: len(dg)==2, fiveclean)][0]
    fiveclean.remove(thethree)
    remains = list(set(thethree) - set(mapl['a']) - set(mapl['f']))
    if len(remains) == 2:
        for l in remains:
            # le charactere est dans b/d
            if l in mapl['d']:
                mapl['d'] = l
                mapl['b'] = list(set(mapl['b']) - set(l))[0]
            else:
                mapl['g'] = l
    mapl['e'] = [x for x in map(lambda dg: list(set(dg)-set([mapl['b'],mapl['d'],mapl['g']])), fiveclean) if x != []][0][0]
    # 6
    mapl['f']= [x for x in map(lambda dg: list(set(dg)-set([mapl[k] for k in ['a','b','d','e','g']])), dgt[6]) if len(x) != 2][0]
    # 8
    mapl['c']= list(set(mapl['c']) - set(mapl['f']))[0]
    nb = ''
    for digit in digits:
        nb += str(computedigi(digit, mapl))
    print (nb)
    return int(nb)
    
    
def process_v2(notes):
    sumnb = 0
    for note in notes:
        sumnb += onelineofnote(note)
    print("fianl sum", sumnb)
        

process_v2(data_exo)
        