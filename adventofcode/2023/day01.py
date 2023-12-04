import utils, sys, re, functools

data_ex= [
    "1abc2",
    "pqr3stu8vwx",
    "a1b2c3d4e5f",
    "treb7uchet",
]
data = utils.readfile("data/d01.txt")

def day01(data):
    r = []
    for line in data:
        title = re.findall('([0-9])', line)
        r.append(int(str(title[0]+""+title[-1])))
    return sum(r)
        
assert day01(data_ex) == 142
print(day01(data))

numbers = {
    "zero":0,
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9
}
def day01_B(data):
    r = []
    for line in data:
        title = re.findall('(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))', line, flags=re.IGNORECASE)
        print(line, ">", title)
        v1 = int(numbers[title[0]]) if title[0] in numbers else int(title[0])
        v2 = int(numbers[title[-1]]) if title[-1] in numbers else int(title[-1])
        s = int(str(v1)+""+str(v2))
        print(s)
        r.append(s)
    return sum(r)

data_ex2 = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen"
]
assert day01_B(data_ex2) == 281

assert day01_B(["eighthree","sevenine"]) == 83 + 79

print(day01_B(data))
