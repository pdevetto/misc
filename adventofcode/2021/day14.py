import utils, sys
data_exemple = ["NNCB",
"",
"CH -> B",
"HH -> N",
"CB -> H",
"NH -> C",
"HB -> C",
"HC -> B",
"HN -> C",
"NN -> C",
"BH -> H",
"NC -> B",
"NB -> B",
"BN -> B",
"BB -> N",
"BC -> B",
"CC -> N",
"CN -> C"]
data_exo = utils.readfile("data/d14.txt")
#print(data_exemple)
#print(data_exo)

def process(data):
    polym = data[0]
    rules = {}
    for rule in data[2:]:
        [ch,c] = rule.split(' -> ')
        if not ch[0] in rules.keys():
            rules[ch[0]] = {}
        rules[ch[0]][ch[1]] = c    
    for step in range(0,10):
        newpolym = ""
        for i in range(0, len(polym)-1):
            #print("for",i)
            newpolym += polym[i]
            if polym[i] in rules.keys():
                if polym[i+1] in rules[polym[i]].keys():
                    newpolym += rules[polym[i]][polym[i+1]]
        newpolym += polym[-1]
        print(newpolym)
        print(len(newpolym))
        polym = newpolym
        count = {}
        for c in polym:
            if not c in count.keys():
                count[c] = 0
            count[c] += 1
        print("step",step)
        print(count)

#process(data_exo)


def setor(tab, e, v = 1):
    if not e in tab.keys():
        tab[e] = 0
    tab[e]+=v
    return tab
    

def process_v2(data):
    polym = data[0]
    rules = {}
    pairs = {}
    for rule in data[2:]:
        [ch,c] = rule.split(' -> ')
        if not ch[0] in rules.keys():
            rules[ch[0]] = {}
        rules[ch[0]][ch[1]] = c    
    for i in range(0, len(polym)-1):
        pairs = setor(pairs, polym[i]+polym[i+1], 1)
    print(pairs)
    for step in range(0,40):
        #19457
        #step 9
        #{'F': 2211, 'H': 2053, 'K': 2040, 'C': 3780, 'O': 1407, 'N': 1270, 'V': 1368, 'S': 2402, 'P': 2289, 'B': 637}
        copypairs = {}
        for pair,nb in pairs.items():
            if pair[0] in rules.keys():
                if pair[1] in rules[pair[0]].keys():
                    lett = rules[pair[0]][pair[1]]
                    setor(copypairs, pair[0]+lett, nb)
                    setor(copypairs, lett+pair[1], nb)
        pairs = copypairs.copy()
        print("step",step)
        print(pairs)
        fco = {}
        for p,v in pairs.items():
            setor(fco, p[1], v)
        print (fco)
            
        
process_v2(data_exo)
