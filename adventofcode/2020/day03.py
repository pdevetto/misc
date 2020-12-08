#! /usr/bin/env python
# -*- coding: utf-8 -*-

import utils, sys

def slope(mymap, h, v):
    ph = 0
    pv = 0
    keep = True
    tree = 0
    while keep:
        ph = (ph + h) % len(mymap[0])
        pv += v
        if pv >= len(mymap):
            keep = False
            return tree
        if mymap[pv][ph] == "#":
            tree += 1
        
            
        
if __name__ == "__main__":
    print("day 03")
    
    mymap = [line for line in utils.getdata("data/d3.txt")]
    
    
    for (i,j) in [(3,1),(1,1),(5,1),(7,1),(1,2)]:
        tr = slope(mymap,i,j)
        print ("slope: ", i, "x",j, "=",tr)
