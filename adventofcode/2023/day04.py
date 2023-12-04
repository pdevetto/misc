import utils, sys, re, functools

data_ex= [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]
data = utils.readfile("data/d_2023_04.txt")

def day04(data):
    gains = 0
    for line in data:
        rx = re.search('Card *[0-9]*: ([0-9 \|]*)', line)
        if rx:
            nbs = [int(n) if n!='|' else '|' for n in rx.groups()[0].strip().split(' ') if n != '']
            thebreak = nbs.index('|') 
            wins,draws = nbs[0:thebreak],nbs[thebreak+1:len(nbs)]
            oknb = [d for d in draws if d in wins]
            if len(oknb) != 0:
                gains += 2 ** (len(oknb)-1)
        else:
            print(line)
    print(gains)
    return gains
        
assert day04(data_ex) == 13
print(day04(data))


def day04_b(data):
    multiplier = {}
    for line in data:
        rx = re.search('Card *([0-9]*): ([0-9 \|]*)', line)
        card = int(rx.groups()[0])
        if rx:
            multiplier[card] = multiplier.get(card, 1)
            nbs = [int(n) if n!='|' else '|' for n in rx.groups()[1].strip().split(' ') if n != '']
            thebreak = nbs.index('|') 
            wins,draws = nbs[0:thebreak],nbs[thebreak+1:len(nbs)]
            oknb = [d for d in draws if d in wins]
            if len(oknb) != 0:
                for i in range(1,len(oknb)+1):
                    multiplier[card+i]=multiplier.get(card+i,1)+multiplier[card]
                print(oknb)
        else:
            print(line)
    scratchcards = sum(multiplier.values())
    print(scratchcards)
    return scratchcards
        
assert day04_b(data_ex) == 30
print(day04_b(data))
