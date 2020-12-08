#! /usr/bin/env python
# -*- coding: utf-8 -*-

import utils, sys

def validatepass_count(chain):
    rule,passw = chain.split(':')
    motiv,letter = rule.strip().split(' ')
    mi,ma = motiv.split('-')    
    cl = passw.count(letter)
    return int(mi) <= cl and cl <= int(ma)
        
def validatepass_pos(chain):
    rule,passw = chain.split(':')
    motiv,letter = rule.strip().split(' ')
    p1,p2 = motiv.split('-')
    #cl = passw.count(letter)
    b = ((passw)[int(p1)] == letter) ^ ((passw)[int(p2)] == letter)
    print( "p1 ",p1," p2 ",p2," let ",letter," l1 ",(" "+passw)[int(p1)]," l2 ", (" "+passw)[int(p2)], " b ",b)
    return b
    

if __name__ == "__main__":
    print("day 02")
    
    countok = 0
    countok2 = 0
    count = 0
    
    validatepass_pos("1-3 a: abcde")
    validatepass_pos("1-3 b: cdefg")
    validatepass_pos("2-9 c: ccccccccc")
    
    for i in utils.getdata("data/d2.txt"):
        print (i)
        count += 1
        if validatepass_count(i):
            countok+= 1
        if validatepass_pos(i):
            countok2+= 1
    print( "count ", count, " ok ", countok, "ok2", countok2 )
