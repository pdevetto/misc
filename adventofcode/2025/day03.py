import utils
import re 

data_ex = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111",
]
data = utils.readfile("data/d03.txt")

def day03(data):
    joltage = []
    for bank in data:
        max_1 = max(bank[:-1])
        max_2 = max(bank[bank.index(max_1)+1:])
        joltage.append(int(str(max_1)+str(max_2)))
    print(joltage)
    return sum(joltage)

assert day03(data_ex) == 357
print(day03(data))

def day03b(data):
    joltage = []
    for bank in data:
        max_i = []
        for i in range(11, 0, -1):
            print(i)
            max_i.append(max(bank[:-i]))
            bank=bank[bank.index(max_i[-1])+1:]
        max_i.append(max(bank))
        joltage.append( int(''.join(max_i)) )
    print(joltage)
    return sum(joltage)

assert day03b(data_ex) == 3121910778619
print(day03b(data))