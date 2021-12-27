import utils, sys
import functools

data_exemple = [""]
data_exo = utils.readfile("data/d24.txt")

##     inp a - Read an input value and write it to variable a.
##     add a b - Add the value of a to the value of b, then store the result in variable a.
##     mul a b - Multiply the value of a by the value of b, then store the result in variable a.
##     div a b - Divide the value of a by the value of b, truncate the result to an integer, then store the result in variable a. (Here, "truncate" means to round the value toward zero.)
##     mod a b - Divide the value of a by the value of b, then store the remainder in variable a. (This is also called the modulo operation.)
##     eql a b - If the value of a and b are equal, then store the value 1 in variable a. Otherwise, store the value 0 in variable a.
    
tlis = [0,1,2]
assert tlis.pop(0) == 0
assert tlis == [1,2]
assert tlis.pop(0) == 1

def process_asm(commands, inputs):
    data = {'w':0,'x':0,'y':0,'z':0}

    def _v(varname):
        if varname in data.keys():
            return data[varname]
        else:
            return int(varname)
    def _s(varname,value):
        data[varname] = int(value)
    
    applied = {
            'inp': lambda a,b: _s(command[1], inputs.pop(0)),
            'add': lambda a,b: _s(command[1], _v(a) + _v(b)),
            'mul': lambda a,b: _s(command[1], _v(a) * _v(b)),
            'div': lambda a,b: _s(command[1], _v(a) / _v(b)),
            'mod': lambda a,b: _s(command[1], _v(a) % _v(b)),
            'eql': lambda a,b: _s(command[1], _v(a) == _v(b)),
        }
    for line in commands:
        if line != '':
            command = (line+' meh').split(' ')
            applied[command[0]](command[1], command[2])
    return data

def find_largest_monad(commands):
    o = int('888'+'699'+'978'+'4'+'9'+'69'+'9')
    # --- 0 > 13  = +8
    # --- 1 > 12  = +7
    # --- 3 > 4   = -3
    # --- 6 > 7   = -2
    # --- 5 > 8   = -1
    # --- 2 > 9   = -7
    # --- 10 > 11 = -6
    a = int('1111')
    lena = 4
    firsta = a
    
    #allas = [ int() for  ]
    i = 0
    mina = -1
    allres = {}
    while i < 100000 and len(str(a)) == lena:
        nb = [int(cc) for cc in str(a)] 
        # biggest 12996997829399
        # lowest 11841231117189
        digits = [str(nb[0]), str(nb[1]), '9', '9','6', '9', '9', '7', '8', '2', '9','3', str(nb[2]), str(nb[3])]
        #digits = [cc for cc in str(a)]
        if not '0' in digits:
            if True:
                res = process_asm(commands, digits)
                i+=1
                print(str(a), "\t\t", res, "\t\t\t", mina)
                if res['z'] < mina or mina == -1:
                    mina = res['z']
        a += 1   
    #print(allres)
    print(firsta, "-  <", a, "  mina", mina) 

from datetime import datetime
a = datetime.now()
find_largest_monad(data_exo)
b = datetime.now()
print(b-a)
