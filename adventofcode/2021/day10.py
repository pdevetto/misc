import utils, sys
data_exemple = ["[({(<(())[]>[[{[]{<()<>>",
"[(()[<>])]({[<{<<[]>>(",
"{([(<{}[<>[]}>{[]{[(<()>",
"(((({<>}<{<{<>}{[]{[]{}",
"[[<[([]))<([[{}[[()]]]",
"[{[{({}]{}}([{[{{{}}([]",
"{<[[]]>}<{[{[{[]{()[[[]",
"[<(<(<(<{}))><([]([]()",
"<{([([[(<>()){}]>(<<{{",
"<{([{{}}[<[[[<>{}]]]>[]]"]
data_exo = utils.readfile("data/d10.txt")
print(data_exemple)
#print(data_exo)

print ('abc'[-1:])
def errchar(line):
    chars = ''
    for c in line:
        #print("c:", c)
        if c in ['<','(','{','[']:
            chars+=c
            #print("---",chars)
        for (cout,cin) in [('>','<'),(')','('),('}','{'),(']','[')]:
            if c == cout:
                #print("test",cin," is ",chars[:-1])
                if chars[-1:] == cin:
                    #print('    correct close',cin," ",cout)
                    chars = chars[0:-1]
                else:
                    #print('    error',cin," ",c)
                    return c
    return chars

def fix(line):
    rline = ""
    for c in line:
        for (cout,cin) in [('>','<'),(')','('),('}','{'),(']','[')]:
            if c == cin:
                rline = cout + rline
    return rline

def lscore(line):
    score = 0
    for c in line:
        for (cout,price) in [('>',4),(')',1),('}',3),(']',2)]:
            if c == cout:
                score = score*5 + price
    return score
        
    
def process(lines):
    score = 0
    rscores = []
    for line in lines:
        #print("#" * 100)
        errc = errchar(line)
        #print("errc", errc)
        if errc == ')': 
            score += 3
        elif errc == ']': 
            score += 57
        elif errc == '}': 
            score += 1197
        elif errc == '>': 
            score += 25137
        else :
            #print("fix", errc)
            rline = fix(errc)
            #print(rline)
            rscore = lscore(rline)
            #print(rscore)
            rscores.append(rscore)
    rscores.sort()
    print(len(rscores))
    indice = int(len(rscores)/2)
    print(indice)
    print(rscores[indice])
    print("xscore", score)    

process(data_exo)