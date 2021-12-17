# -*- coding: utf-8 -*-

from utils import *

def depth_analysis_V1(measures=[]):
    increases = 0
    last_measure, *measures = measures
    while len(measures) > 0:
        measure,*measures = measures
        if last_measure != -1:
            if int(measure) > int(last_measure) :
                increases += 1
        #print(last_measure, ",", measure, ",", increases)
        last_measure = measure
        
    return increases

def depth_analysis_V2(measures=[]):
    increases = 0
    m0, *measures = measures
    m1, *measures = measures
    m2, *measures = measures
    while len(measures) > 0:
        m3, *measures = measures
        if int(m1)+int(m2)+int(m3) > int(m0)+int(m1)+int(m2) :
            increases += 1
        #print(last_measure, ",", measure, ",", increases)
        m0 = m1
        m1 = m2 
        m2 = m3
    return increases


R = depth_analysis_V1([199,200,208,210,200,207,240,269,260,263])
print (R)
a = file_input("/home/pierre/organisation/misc/advent21/data/d01test.txt")
R = depth_analysis_V1(a)
print (R)

#--------------

R = depth_analysis_V2([199,200,208,210,200,207,240,269,260,263])
print (R)
a = file_input("/home/pierre/organisation/misc/advent21/data/d01test.txt")
R = depth_analysis_V2(a)
print (R)