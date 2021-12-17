import utils

data_exemple = ["7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
                "","22 13 17 11  0"," 8  2 23  4 24","21  9 14 16  7"," 6 10  3 18  5"," 1 12 20 15 19",
                ""," 3 15  0  2 22"," 9 18 13 17  5","19  8  7 25 23","20 11 10 24  4","14 21 16 12  6",
                "","14 21 17 24  4","10 16 15  9 19","18  8 23 26 20","22 11 13  6  5"," 2  0 12  3  7"]
data_exo = utils.readfile("data/d04.txt")

def parse_data(inputs):
    tirage, *cards_data = inputs
    tirage = [i for i in map(lambda x: x.strip(), tirage.split(","))]
    
    cards = []
    tempcard = []
    for line in cards_data:
        if len(line.strip()) == 0:
            if len(tempcard) != 0:
                cards.append(tempcard)
                tempcard = []
        else:
            #print ("tline", line, " l: ", len(line), " - ", tempcard)
            tline = [ i for i in map(lambda x: x, filter(lambda x: len(x)!=0, line.strip().split(" "))) ]
            tempcard.append(tline )
    cards.append(tempcard)
    for card in cards:
        pass 
        #print (card)
    return tirage, {i:v for i,v in enumerate(cards)}

def iswin(card):
    for line in card:
        if len([x for x in filter(lambda case: case[0] != "*", line)]) == 0:
            return True
    for i in range(len(card[0])):
        if sum([1 for x in range(0, len(card)) if card[x][i][0] != "*"]) == 0:
            return True
    return False

assert iswin([["*1", "*2", "*3", "*4", "*5"]])
assert not iswin([["*1", "*2", "*3", "*4", "5"],["1", "2", "3", "4", "5"]])
assert iswin([["*1", "2", "3", "*4", "*5"],["*1", "2", "3", "4", "5"]])

def count(card):
    score = 0
    for line in card:
        print("line", line)
        score += sum([x for x in map(lambda x: int(x) if x[0]!="*" else 0, line)])
        print("score", score)
    return score
        
assert count([["*1", "2", "*3", "*4", "5"], ["*6","*7","*8","*9","10"]]) == 17

def tir(card, tirage):
    for i,line in enumerate(card):
        card[i] = [ x for x in map(lambda case: "*"+case if case==tirage else case, line)]
    return card

print(tir([["1", "2", "3", "4", "5"]], "1"))
assert tir([["1", "2", "3", "4", "5"]], "1") == [["*1", "2", "3", "4", "5"]]

def play(tirage, cards):
    win = {}
    for i in tirage:
        print("tirage", i)
        for n, card in cards.items():
            newcard = tir(card,i)
            cards[n] = newcard
            if not n in win and iswin(cards[n]):
                #return i, count(card)
                win[n] = 1
                if len(cards) == len(win):
                    print("last_board")
                    return i, count(card)
                
    
tirage, cards = parse_data(data_exo)
i,s = play(tirage, cards)

print("tir", i, " board score", s, " = ", int(i)*int(s))