#! /usr/bin/env python
# -*- coding: utf-8 -*-

import utils, sys, re

def count_answer_everyone(answers):
    if len(answers) == 1:
        return len(answers[0])
    base = [l for l in answers[0]]
    for word in answers[1:]:
        base = list(set(base) & set([l for l in word])) 
        if len(base) == 0:
            return 0
    return len(base)

###########

def tests():
    assert count_answer_everyone(["abc"]) == 3
    assert count_answer_everyone(["a","b","c"]) == 0
    assert count_answer_everyone(["ab","b","abd"]) == 1
    

###########

if __name__ == "__main__":
    tests()
    print("day 06")
    total_anyone = 0
    group = ""
    total_everyone = 0
    answers = []
    
    ## DOn't forget to put one line at the end
    for line in utils.getdata("data/d6.txt"):
        if line.strip() == "":
            count = len(set([letter for letter in group]))
            total_anyone += count
            #print(group,"=",count)
            group = ""
            
            total_everyone += count_answer_everyone(answers)
            answers = []
        else:
            group += line.strip()
            answers.append(line.strip())
    print("total_anyone", total_anyone)
    print("total_everyone", total_everyone)
