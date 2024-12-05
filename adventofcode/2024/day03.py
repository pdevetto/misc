import utils, re

data_ex = []
data = utils.readfile("data/day03.txt")


def day03(data):
    sum = 0
    for line in data:
        muls = re.findall("mul\([0-9]*,[0-9]*\)", line)
        for mul in muls:
            xy = re.findall("mul\(([0-9]*),([0-9]*)\)", mul)
            sum += int(xy[0][0]) * int(xy[0][1])
    return sum


assert day03(["mul(4*"]) == 0
assert day03(["mul(6,9!"]) == 0
assert day03(["?(12,34)"]) == 0
assert day03(["( 2 , 4 )"]) == 0
assert (
    day03(["xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"])
    == 161
)

print(day03(data))


def day03b(data):
    sum = 0
    enable = True
    for line in data:
        muls = re.findall("mul\([0-9]*,[0-9]*\)|do\(\)|don't\(\)", line)
        for mul in muls:
            if mul == "do()":
                enable = True
            elif mul == "don't()":
                enable = False
            elif enable:
                xy = re.findall("mul\(([0-9]*),([0-9]*)\)", mul)
                sum += int(xy[0][0]) * int(xy[0][1])
    return sum


assert (
    day03b(
        ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]
    )
    == 48
)
print(day03b(data))
