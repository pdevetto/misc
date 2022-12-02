import utils, sys
import functools

data_exemple = ["A Y","B X","C Z"]
data = utils.readfile("data/d2.txt")

#print(data_exemple)
#print(data) 

def d020(data):
    #print(data)
    win = ["RS", "SP", "PR"]
    score = {"R":1, "P":2, "S":3}
    forces = {"A":"R", "B":"P", "C":"S", "X":"R", "Y":"P", "Z":"S"}
    totalscore = 0
    for line in data: 
        [a,b] = line.split(" ")
        #print(a, "-", b)
        roundscore = score[forces[b]]
        fa,fb = forces[a],forces[b]
        if fa == fb:
            roundscore += 3
        elif fb+""+fa in win:
            roundscore += 6
        #print("R : ", roundscore)
        totalscore += roundscore
    print("Total : ", totalscore)

def d022(data):
    #print(data)
    win = {"R":"P", "S":"R", "P":"S"}
    score = {"R":1, "P":2, "S":3}
    forces = {"A":"R", "B":"P", "C":"S"}
    totalscore = 0
    for line in data: 
        [a,b] = line.split(" ")
        #print(a, "-", b)
        roundscore = 0
        fa = forces[a]
        if b == "Y":
            roundscore += score[fa] + 3
        elif b == "Z":
            roundscore += score[win[fa]]+ 6
        else: 
            lose = list(set(["R", "P", "S"]) - set([fa, win[fa]]))
            roundscore += score[lose[0]]
        #print("R : ", roundscore)
        totalscore += roundscore
    print("Total : ", totalscore)
    
res = d022(data_exemple)

res2 = d022(data)


