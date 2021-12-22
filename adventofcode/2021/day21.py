import json, re
from collections import Counter
    
def readfile(path):
    print(path)
    with open(path) as f:
        content = f.read().splitlines()
        return content

#data_exo = readfile("data/d21.txt")
data_exemple=[""]

#print(data_exemple)
#print(data_exo)

die = 0

def rolldice(die):
    die += 1
    if die == 101:
        die = 1
    return die

def play(player):
    die = 0
    roll = 0
    score = {1:0,2:0}
    while True:
        for j,pos in player.items():
            #print(f"j {j}")
            susu = 0
            for i in range(0,3):
                roll += 1
                die += 1
                if die == 101:
                    die = 1
                susu += die
                #print(f"die {die}")
            newpos = (pos + susu) % 10
            newpos = 10 if newpos == 0 else newpos
            #print(f"pos {pos} susu{susu} new{newpos}")
            player[j] = newpos
            score[j] += newpos
            if score[j] >= 1000:
                return score, roll

def possiblescores():
    sums = []
    count = {}
    for dice in range(0,3):
        newsums = []
        for univ in range(1,4):
            if dice == 0:
                newsums.append(univ)
            for susum in sums:
                thesum = univ + susum
                newsums.append(thesum)
                if dice == 2:
                    count[thesum] = count.get(thesum,0) + 1
        sums = newsums
    return count

print(possiblescores())

def getuniverse(pos1,score1,pos2,score2):
    return f"{pos1}.{score1}_{pos2}.{score2}"
def getdata(univ):
    s1,s2 = univ.split('_')
    pos1,score1 = s1.split('.')
    pos2,score2 = s2.split('.')
    return int(pos1),int(score1),int(pos2),int(score2)


def play2(player):
    universes = {
        getuniverse(player[1],0,player[2],0):1
    }
    print(universes)
    i = 0
    backagain = 5
    pp = 2
    while backagain > 0:
        print(i," back:", backagain)
        if pp == 2:
            pp=1
        else:
            pp=2
        backagain = 0
        i += 1
        new_universes = {}
        for one_univ,count in universes.items():
            pos1,score1,pos2,score2 = getdata(one_univ)
            if score1 < 21 and score2 < 21:
                backagain += 1
                bigscore = 0
                [pos,score] = {1:[pos1,score1],2:[pos2,score2]}[pp]
                #print("J", pp,"val",pos,score)
                for susum,possible in {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}.items():
                    newpos = (pos + susum) % 10
                    newpos = 10 if newpos == 0 else newpos
                    if pp == 1:
                        uniid = getuniverse(newpos,score+newpos,pos2,score2)
                    else:
                        uniid = getuniverse(pos1,score1,newpos,score+newpos)
                    new_universes[uniid] = new_universes.get(uniid,0) + count*possible
            else:
                new_universes[one_univ] = new_universes.get(one_univ, 0) ++ count
        universes = new_universes
        #print("unisize",universes)
        print(len(universes))
    #print(universes)
    return universes
            
                        
                
#print(play({1:4,2:8}))
#print(play({1:6,2:9}))
universes = play2({1:4,2:8})
#print(play2({1:6,2:9}))
universes = play2({1:6,2:9})

bigsco1 = 0
bigsco2 = 0

for key, count in universes.items():
    pos1,score1,pos2,score2 = getdata(key)
    
    if score1 >= 21 and score2 >= 21:
        sys.exit()
    if score1 >= 21:
        bigsco1 += count
    if score2 >= 21:
        bigsco2 += count
print (bigsco1)
print (bigsco2)
        
