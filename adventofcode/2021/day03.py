import utils

def common_bits(bits):
    size = len(bits)
    count = {}
    for nbit in bits:
        for i,bit in enumerate([n for n in nbit]):
            if not i in count:
                count[i] = 0
            count[i] += int(bit)
    print(size, count)
    freq = ""
    lfreq = ""
    for i,v in count.items():
        freq += "1" if v > size/2 else "0"
        lfreq += "1" if v < size/2 else "0"
    print (freq)
    print (lfreq)
    
            
data_exemple = ["00100","11110","10110","10111","10101","01111","00111","11100","10000","11001","00010","01010"]
data_exo = utils.readfile("data/d03.txt")
common_bits(data_exemple)
common_bits(data_exo)

def leastmost_common_bits_col(bits, i, leastmost):
    size = len(bits)
    count = 0
    for nbit in bits:
        count += int(nbit[i])
    if leastmost == 1:
        return 1 if count >= size/2 else 0
    else:
        return 0 if count >= size/2 else 1

for i in range (0,5):
    a = leastmost_common_bits_col(["00100","11110","10110","10111","10101","01111","00111","11100","10000","11001","00010","01010"], i, 1)
    print(a)
for i in range (0,7):
    a = leastmost_common_bits_col(utils.readfile("data/d03.txt"), i, 1)
    print(a)
    

def oxygen(numbers, leastmost):
    bit_pos = 0
    #print(numbers)
    number_most = [ x for x in numbers ]
    for i in range(0, len(numbers[0])):
        most = leastmost_common_bits_col(number_most, bit_pos, leastmost)
        #print ("most", most)
        number_most = [ x for x in filter(lambda number: number[bit_pos] == str(most), number_most)]
        #print ("number most", number_most)
        if len(number_most) == 1:
            return number_most[0]
        bit_pos += 1
        
    
      
    
    
n = oxygen(data_exemple, 1)
print(n, ",",  int(str(n),2))
n = oxygen(data_exemple, 0)
print(n, ",",  int(str(n),2))
n = oxygen(data_exo, 1)
print(n, ",",  int(str(n),2))
n = oxygen(data_exo, 0)
print(n, ",", int(str(n),2))
