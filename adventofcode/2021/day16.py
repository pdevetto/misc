import utils, sys
import functools
data_exemple = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060"]
    #"8A004A801A8002F478","620080001611562C8802118E34","C0015000016115A2E0802F182340","A0016C880162017C3686B18A3D4780"]
data_exo = utils.readfile("data/d16.txt")
#print(data_exemple)
#print(data_exo)

def hextobin(word):
    return ''.join([str(bin(int(l,16)))[2:].zfill(4) for l in word])

def paquet(w, niv=0):
    version = 0
    print(niv* "--","######################")
    v= w[0:3]
    typid = int(w[3:6],2)
    print(niv* "--", f"vers {int(v,2)}")
    print(niv* "--", f"type {typid}")
    version += int(v,2)
    if typid == 4:
        keep = True
        nb = ""
        ch = 6
        while keep:
            print(niv* "--",f"c{w[ch]} w {w[ch+1:ch+5]}")
            if w[ch] == "1":
                keep = True
            else: 
                keep = False
            nb += w[ch+1:ch+5]
            ch += 5
        ll = (int(ch/4)+1)*4
        print(niv* "--",f"    n: {int(nb,2)} l: {ch} ll: {ll}")
        return int(nb,2), ch, version
    else:
        lenty = w[6]
        if lenty == "1":
            nsub = int(w[7:18],2)
            print(niv* "--",f"nsub{nsub}")
            ch = 18
            npaq = 0
            subp = []
            while npaq<nsub:
                n, le, nvv = paquet(w[ch:], niv+1)
                version += nvv
                print(niv* "--","NSUB : ",n," of l=",le)
                subp.append(n)
                npaq += 1
                ch += le
                
            return operat(typid,subp), ch, version
        else:
            tlen = w[7:22]
            print(niv* "--",f"tlen{tlen} => {int(tlen,2)}")
            ch = 22
            end = (22 + int(tlen,2))
            subp = []
            while ch < end:
                n, le, nvv = paquet(w[ch:end], niv+1)
                version += nvv
                print(niv* "--","TLEN : ",n," of l=",le)
                subp.append(n)
                ch += le
            return operat(typid,subp), end, version
            
    return 0,0

def operat(tid,vals):
    if tid == 0:
        return sum(vals)
    if tid == 1:
        if len(vals) == 1:
            return vals[0]
        else:
            print(vals)
            return functools.reduce(lambda a, b: a*b, vals)
    if tid == 2:
        return min(vals)
    if tid == 3:
        return max(vals)
    if tid == 5:
        return 1 if vals[0] > vals[1] else 0
    if tid == 6:
        return 1 if vals[0] < vals[1] else 0
    if tid == 7:
        return 1 if vals[0] == vals[1] else 0
    
    
#    Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
#    Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
#    Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
#    Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
#    Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; 
#otherwise, their value is 0. These packets always have exactly two sub-packets.
#    Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; 
#otherwise, their value is 0. These packets always have exactly two sub-packets.
#    Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; 
#otherwise, their value is 0. These packets always have exactly two sub-packets.



["D2FE28",
    "38006F45291200",
    "EE00D40C823060",
 "8A004A801A8002F478","620080001611562C8802118E34",
 "C0015000016115A2E0802F182340","A0016C880162017C3686B18A3D4780"]
data_exemple = ["A0016C880162017C3686B18A3D4780"]
    
for w in data_exo:
    paq = hextobin(w)
    print(w)
    n,length,versions = paquet(paq)
    print ("Versions", versions)
    print (n)
    