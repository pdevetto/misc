import utils, sys
import functools
data_exemple = [
""]
    #"8A004A801A8002F478","620080001611562C8802118E34","C0015000016115A2E0802F182340","A0016C880162017C3686B18A3D4780"]
data_exo = utils.readfile("data/d17.txt")
#print(data_exemple)
#print(data_exo)


def testarea(tgtx, tgty, x, y):
    ax, bx = tgtx.split('..')
    ay, by = tgty.split('..')
    return int(ax) <= x and x <= int(bx) and int(ay) <= y and y <= int(by)

assert testarea("0..10", "0..10", 5, 5) == True
assert testarea("0..10", "0..10", 5, 11) == False
assert testarea("0..10", "0..10", 11, 5) == False
assert testarea("0..10", "0..10", 0, 10) == True
assert testarea("0..10", "0..10", -10, -10) == False
    
def process(tgtx, tgty):
    within = 0
    ax, bx = tgtx.split('..')
    ay, by = tgty.split('..')
    ax, bx, ay, by = int(ax), int(bx), int(ay), int(by)
    for vx in range(-3*bx,bx+1):
        twithin = 0
        for factor in [+1, -1]:
            if factor == +1:
                vy = 0
            else:
                vy = -1
            nobreakx = True
            while nobreakx:
                cvx = vx
                cvy = vy
                x,y = 0,0
                highery = 0
                yys = []
                #print("########################")
                keep = True
                step = 0
                while keep:
                    step += 1
                    keep = True
                    x += cvx
                    lasty = y
                    if y > highery:
                        highery = y
                    y += cvy
                    yys.append(y)
                    cvx += (-1 if cvx > 0 else (1 if cvx < 0 else 0))
                    cvy -= 1
                    #print (f"n {x} {y}  \t        {cvx} {cvy}     step {step}")
                    if testarea(tgtx, tgty, x, y): 
                        #print("###")
                        #print(f"#{vx},{vy}    \t\t\ŧ |  x{x} in {tgtx} |  y{y} in {tgty}  |   step {step} |  HY :  {highery}")
                        #print(yys)
                        within += 1
                        twithin += 1
                        keep = False
                        #return vx, vy
                    nfil = 4
                    if (bx > 0 and x > bx):
                        keep = False
                    if (ay < 0 and y < ay):
                        if cvy < 0:
                            keep = False
                        if lasty >= 0:
                            nobreakx = False
                    
                vy += factor
                if vy > 1000 or vy < -1000:
                    nobreakx = False
        if twithin != 0:
            print (vx, twithin)
    return within
                    
            

res = process( "20..30", "-10..-5" )
print(res)
assert res == 112
res = process( "207..263", "-115..-63")
print(res)