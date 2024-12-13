import utils, re

data_ex = [
    "190: 10 19",
    "3267: 81 40 27",
    "83: 17 5",
    "156: 15 6",
    "7290: 6 8 6 15",
    "161011: 16 10 13",
    "192: 17 8 14",
    "21037: 9 7 18 13",
    "292: 11 6 16 20",
]
data = utils.readfile("data/day07.txt")


def calibr8(result, numbers, third=False):
    calculus = [numbers[0]]
    for numb in numbers[1:]:
        calculus_next = []
        for calc in calculus:
            # Addition
            op_add = calc + numb
            if op_add <= result:
                calculus_next.append(op_add)
            # Multiplication
            op_mul = calc * numb
            if op_mul <= result:
                calculus_next.append(op_mul)
            # Concatenation
            if third:
                op_con = int(str(calc) + "" + str(numb))
                if op_con <= result:
                    calculus_next.append(op_con)
        calculus = calculus_next
    return calculus.count(result)


assert calibr8(190, [10, 19]) == 1
assert calibr8(3267, [81, 40, 27]) == 2
assert calibr8(292, [11, 6, 16, 20]) == 1
assert calibr8(161011, [16, 10, 13]) == 0

assert calibr8(156, [15, 6]) == 0
assert calibr8(156, [15, 6], True) == 1
assert calibr8(7290, [6, 8, 6, 15]) == 0
assert calibr8(7290, [6, 8, 6, 15], True) == 1
assert calibr8(192, [17, 8, 14]) == 0
assert calibr8(192, [17, 8, 14], True) == 1


def day07(data, third=False):
    sum_calculus = 0
    for line in data:
        result, numbers = line.split(":")
        result = int(result)
        numbers = list(
            map(lambda ns: int(ns.strip()), filter(None, numbers.split(" ")))
        )
        if calibr8(result, numbers, third) > 0:
            sum_calculus += result
    print(sum_calculus)
    return sum_calculus


assert (day07(data_ex)) == 3749
print(day07(data))

assert (day07(data_ex, True)) == 11387
print(day07(data, True))
