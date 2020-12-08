#! /usr/bin/env python
# -*- coding: utf-8 -*-

import utils, sys, pprint, re

def test_passport(passport):
    print("test" + passport)
    field = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
    having = list(map(lambda x: x.strip().split(':')[0], passport.split(' ')))
    
    #print(having)
    missing = [fie for fie in field if not fie in having]
    if missing == ['cid'] or missing == []:
        return 1
    else:
        print ("==> miss ", ",".join(missing))
        return 0
        

###########

def valid_int(mape,val,mini,maxi):
    try: 
        intval = int(mape[val])
        ii = intval >= mini and intval <= maxi
        if not ii:
            print("Wring int value ", val, " m:", mini, " M:", maxi, " =", intval)
        return ii
    except Exception:
        print("INT no ", val)
        return False

def valid_hgt(mape,val):
    try:
        hgt = mape[val]
        unit = hgt[-2:]
        intval = int(hgt[0:-2])
        if unit == "cm":
            return intval >= 150 and intval <= 193
        elif hgt[-2:] == "in":
            return intval >= 59 and intval <= 76
    except Exception:
        pass
    return False

def valid_ecl(mape, val):
    try:
        return mape[val] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    except Exception:
        return False

def valid_reg(mape, val, regexp):
    p = re.compile(regexp)
    try:
        return p.match(mape[val]) != None
    except Exception:
        return False

###########

def validate_passport(passport):
    print("val" + passport)
    field = ['byr','iyr','eyr','hgt','hcl','ecl','pid','cid']
    mape = {}
    for elt in passport.split(' '):
        if len(elt.split(':')) != 2:
            print(elt)
        else:
            mape[elt.split(':')[0].strip()] = elt.split(':')[1].strip()
        
    print ( mape )
    return (
        valid_int(mape, "byr",1920,2002) and 
        valid_int(mape, "iyr",2010,2020) and
        valid_int(mape, "eyr",2020,2030) and
        valid_hgt(mape, "hgt") and 
        valid_ecl(mape, "ecl") and 
        valid_reg(mape, "hcl", "^#[0-9a-f]{6}$") and
        valid_reg(mape, "pid", "^[0-9]{9}$")
    )

###########

def tests():
    mape = {
        "byr1": 2002, "byr2": "2002", "byr3":2003,
        "hgt1": "60in", "hgt2": "190cm", "hgt3": "190in", "hgt4": 190,
        "hcl1":"#123abc", "hcl2":"#123abz", "hcl3":"123abc", 
        "ecl1": "brn", "ecl2": "wat",
        "pid1": "000000001", "pid2": "0123456789"
    }
    
    assert valid_int(mape,"byr1",1920,2002)
    assert valid_int(mape,"byr2",1920,2002)
    assert not valid_int(mape,"byr3",1920,2002)
    
    assert valid_hgt(mape, "hgt1")
    assert valid_hgt(mape, "hgt2")
    assert not valid_hgt(mape, "hgt3")
    assert not valid_hgt(mape, "hgt4")

    assert valid_reg(mape, "hcl1", "#[0-9a-f]{6}")
    assert not valid_reg(mape, "hcl2", "#[0-9a-f]{6}")
    assert not valid_reg(mape, "hcl2", "#[0-9a-f]{6}")

    
    assert valid_ecl(mape, "ecl1")
    assert not valid_ecl(mape, "ecl2")
    
    assert valid_reg(mape, "pid1", "[0-9]{9}")
    assert not valid_reg(mape, "pid2", "^[0-9]{9}$")

###########

if __name__ == "__main__":
    tests()
    print("day 04")
    ok = 0
    ok2 = 0
    passport = ""
    
    for line in utils.getdata("data/d4.txt"):
        print ("######################################################")
        if line.strip() == "":
            #print("blank", line.strip() , "-")
            #ok += test_passport(passport)
            ok2 += 1 if validate_passport(passport) else 0
            passport = ""
        else:
            #print( "not blank", line.strip() , "-")
            passport += " " + line
    
    print (ok2, " ok pass V2")
