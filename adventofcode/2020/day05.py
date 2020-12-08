#! /usr/bin/env python
# -*- coding: utf-8 -*-

import utils, sys, pprint, re, math

def lower_half(a,b):
    return a, math.floor(b - (b-a)/2)

def upper_half(a,b):
    return math.ceil(a + (b-a)/2), b

def find_seat(chain):
    row,row_z = 0,127
    col,col_z = 0,7
    for cha in chain:
        if cha == "F":
            row,row_z = lower_half(row,row_z)
        if cha == "B":
            row,row_z = upper_half(row,row_z)
        if cha == "R":
            col,col_z = upper_half(col,col_z)
        if cha == "L":
            col,col_z = lower_half(col,col_z)
    
    return row * 8 + col

def tests():
    print("tests")
    
    assert (lower_half(0,127)) == (0,63)
    assert (upper_half(0,63)) == (32,63)
    assert (lower_half(32,63)) == (32,47)
    assert (upper_half(32,47)) == (40,47)
    assert (upper_half(40,47)) == (44,47)
    assert (lower_half(44,47)) == (44,45)
    assert (lower_half(44,45)) == (44,44)
    
    assert (upper_half(0,7)) == (4,7)
    assert (lower_half(4,7)) == (4,5)
    assert (upper_half(4,5)) == (5,5)
    
    print (find_seat("FBFBBFFRLR"))
    assert find_seat("FBFBBFFRLR") == 357

if __name__ == "__main__":
    tests()
    print("day 05")
        
    all_seats = list(range(50,1024))
    max_seat = -1
    for line in utils.getdata("data/d5.txt"):
        seat = find_seat(line)
        print ("##### ",line, " => ", seat)
        max_seat = max(seat, max_seat)
        
        all_seats.remove(seat)
    print("MAX : ", max_seat)
    print("all seats left")
    print(all_seats)
